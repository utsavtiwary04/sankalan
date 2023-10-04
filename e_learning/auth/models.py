from django.db import models
from __common__.base_model import BaseModelMixin
from __common__ import redis_client

import json
import datetime

class CampaignStatus(models.TextChoices):
    INACTIVE = 'inactive'
    ACTIVE   = 'active'

class User(BaseModelMixin):
    name          = models.CharField(max_length=64, null=False, blank=False)
    phone         = models.CharField(max_length=20, null=False, blank=False)
    email         = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return f"{self.id} {self.name} ({self.phone} | {self.email})"
