from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save
from __common__.base_model import BaseModelMixin
from __common__.redis_client import RedisC
from __common__ import CSV
from .tasks import prepare_master_price

import json
import datetime

class CampaignStatus(models.TextChoices):
    INACTIVE = 'inactive'
    ACTIVE   = 'active'

class CampaignType(models.TextChoices):
    COUPON = 'coupon'
    DIRECT = 'direct'

class Campaign(BaseModelMixin):
    name        = models.CharField(max_length=64, null=False, blank=False)
    description = models.CharField(max_length=200, null=False, blank=False)
    created_by  = models.ForeignKey('users.User', null=True, blank=False, on_delete=models.SET_NULL)
    type        = models.CharField(max_length=64, null=False, blank=False, default=CampaignType.DIRECT)
    start_date  = models.DateTimeField(blank=True, null=True)
    end_date    = models.DateTimeField(blank=True, null=True)
    status      = models.CharField(
                                    max_length  = 64,
                                    choices     = CampaignStatus.choices,
                                    default     = CampaignStatus.INACTIVE,
                                    null        = False, 
                                    blank       = False
                                )
    product_segment = models.ForeignKey('ProductSegment', null=True, blank=True, on_delete=models.SET_NULL)
    user_segment    = models.ForeignKey('UserSegment', null=True, blank=True, on_delete=models.SET_NULL)

    @staticmethod
    def active_campaign(campaign_id):
        return Campaign.objects.filter(id=campaign_id).filter(deleted_at=None).first()

    def course_ids(self):
        if self.product_segment is None:
            return []
        return self.product_segment.user_ids()

    def user_ids(self):
        if self.user_segment is None:
            return []
        return self.user_segment.user_ids()

    def __str__(self):
        return f"Campaign {self.type} {self.name} :: {self.status}"

    def has_ended(self):
        if (self.start_date is not None) and (self.end_date is not None):
            return not (self.start_date <= datetime.datetime.now().astimezone() <= self.end_date)
        return False

@receiver(post_save, sender=Campaign)
def campaign_post_save(sender, instance, **kwargs):
    prepare_master_price.delay(instance.id)



class ProductSegment(BaseModelMixin):
    name          = models.CharField(max_length=64, null=False, blank=False)
    description   = models.CharField(max_length=200, null=False, blank=False)
    created_by    = models.ForeignKey('users.User', null=True, blank=False, on_delete=models.SET_NULL)
    product_count = models.IntegerField(null=True, blank=False, default=0)
    file_url      = models.CharField(max_length=200, null=True, blank=True)
    # category      = models.ForeignKey('Category', null=True, blank=True)
    segment_key   = models.CharField(max_length=200, null=False, blank=False)

    @property
    def product_ids(self):
        return [int(i) for i in RedisC().smembers(self.segment_key)]

    @staticmethod
    def generate_segment_key(segment_name):
        return f"PRODUCTS_{segment_name}_{int(datetime.datetime.now().timestamp())}"

    def __str__(self):
        return f"{self.name} ({self.product_count} products) for campaign"

    def product_prices_from_source(self):
        return CSV(self.file_url).data()

@receiver(post_save, sender=ProductSegment)
def product_segment_post_save(sender, instance, **kwargs):
    if not instance._product_ids:
        return

    RedisC().sadd(instance.segment_key, *set(instance._product_ids))



class UserSegment(BaseModelMixin):
    name         = models.CharField(max_length=64, null=False, blank=False)
    description  = models.CharField(max_length=200, null=False, blank=False)
    created_by   = models.ForeignKey('users.User', null=True, blank=False, on_delete=models.SET_NULL)
    user_count   = models.IntegerField(null=True, blank=False, default=0)
    file_url     = models.CharField(max_length=200, null=True, blank=True)
    segment_key  = models.CharField(max_length=200, null=False, blank=False)

    @property
    def user_ids(self):
        return [int(i) for i in RedisC().smembers(self.segment_key)]

    def __str__(self):
        return f"{self.name} ({self.user_count} users) for campaign"

    @staticmethod
    def generate_segment_key(segment_name):
        return f"USERS_{segment_name}_{int(datetime.datetime.now().timestamp())}"

@receiver(post_save, sender=UserSegment)
def user_segment_post_save(sender, instance, **kwargs):
    if not instance._user_ids:
        return

    RedisC().sadd(instance.segment_key, *set(instance._user_ids))
