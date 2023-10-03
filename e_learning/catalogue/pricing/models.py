from django.db import models
from __common__.base_model import BaseModelMixin
from __common__ import redis_client

import json
import datetime

class CampaignStatus(models.TextChoices):
    INACTIVE = 'inactive'
    ACTIVE   = 'active'


class Campaign(BaseModelMixin):
    # duration = models.IntegerField(null=True, blank=False, default=DEFAULT_SESSION_DURATION)
    name        = models.CharField(max_length=64, null=False, blank=False)
    description = models.CharField(max_length=200, null=False, blank=False)
    # created_by = models.ForeignKey('User', null=False, blank=False)
    type        = models.CharField(max_length=64, null=False, blank=False)
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

    def __str__(self):
        return f"""Campaign {self.type} {self.name} :: {self.status}
                   ({self.start_date.strftime("%a, %-d %b %Y") - self.end_date.strftime("%a, %-d %b %Y")})"""

    def is_active(self):
        return self.start_date <= datetime.datetime.now().astimezone() <= self.end_date



class ProductSegment(BaseModelMixin):
    name          = models.CharField(max_length=64, null=False, blank=False)
    description   = models.CharField(max_length=200, null=False, blank=False)
    # created_by    = models.ForeignKey('User', null=False, blank=False, on_delete=models.SET_NULL)
    product_count = models.IntegerField(null=True, blank=False, default=0)
    file_url      = models.CharField(max_length=200, null=True, blank=True)
    category      = models.ForeignKey('Category', null=True, blank=True)
    segment_key   = models.CharField(max_length=200, null=False, blank=False)
    campaign      = models.ForeignKey('Campaign', null=True, blank=True, on_delete=models.SET_NULL)

    @property
    def product_ids(self):
        return redis_client().smembers(self.segment_key)

    def __str__(self):
        return f"{self.name} ({self.product_count} products) for campaign {self.campaign}"

    def clean(self):
        if self.category and self.course:
            raise ValidationError("Product Segment can have either a course or a category")



class UserSegment(BaseModelMixin):

    name         = models.CharField(max_length=64, null=False, blank=False)
    description  = models.CharField(max_length=200, null=False, blank=False)
    # created_by   = models.ForeignKey('User', null=False, blank=False, on_delete=models.SET_NULL)
    user_count   = models.IntegerField(null=True, blank=False, default=0)
    file_url     = models.CharField(max_length=200, null=True, blank=True)
    segment_key  = models.CharField(max_length=200, null=False, blank=False)
    campaign     = models.ForeignKey('Campaign', null=True, blank=True, on_delete=models.SET_NULL)

    @property
    def user_ids(self):
        return redis_client().smembers(self.segment_key)

    def __str__(self):
        return f"{self.name} ({self.user_count} users) for campaign {self.campaign}"
