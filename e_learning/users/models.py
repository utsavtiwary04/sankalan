from django.db import models
from __common__.base_model import BaseModelMixin
from __common__ import redis_client

import json
import datetime

class User(BaseModelMixin):
    name          = models.CharField(max_length=64, null=False, blank=False)
    phone         = models.CharField(max_length=20, null=False, blank=False)
    email         = models.CharField(max_length=200, null=True, blank=True)

    class Meta:
        verbose_name        = "e_learning users"
        verbose_name_plural = "e_learning_users"

    ## Commonly used queries as methods
    @staticmethod
    def active_user(user_id):
        return User.objects.filter(id=user_id).filter(deleted_at=None).first()

    def __str__(self):
        return f"{self.id} {self.name} ({self.phone} | {self.email})"

    def full_name(self):
        return self.name

