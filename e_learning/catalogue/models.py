from django.db import models
from django.core import serializers
from django.utils.translation import gettext_lazy as _
from __common__.base_model import BaseModelMixin
from django.contrib.postgres.fields import ArrayField

import uuid
import json
import datetime

def generate_course_code():
    return f"CPN{str(uuid.uuid4())[:8]}"

class CourseStatus(models.TextChoices):
    INACTIVE                = 'inactive'
    ACCEPTING_REGISTRATIONS = 'accepting_registrations'
    PAUSED_REGISTRATIONS    = 'paused_registrations'
    ENDED                   = 'ended'


class Course(BaseModelMixin):

    DEFAULT_SESSION_COUNT    = 10
    DEFAULT_SESSION_DURATION = 90
    DEFAULT_MAX_SEATS        = 25
    DEFAULT_AMOUNT           = 99.0

    # https://stackoverflow.com/questions/3936182/using-a-uuid-as-a-primary-key-in-django-models-generic-relations-impact TODO
    id                  = models.AutoField(primary_key=True)
    heading             = models.CharField(max_length=64, null=False, blank=False)
    description         = models.TextField(max_length=2000, null=True, blank=True)
    # teacher_id            = models.CharField(max_length=64, null=False, blank=False)  #unique true
    amount              = models.DecimalField(
                                    decimal_places=2, 
                                    default=DEFAULT_AMOUNT, 
                                    max_digits=8, 
                                    null=False, 
                                    blank=False
                                )
    currency            = models.CharField(
                                    max_length=20, 
                                    default="INR", 
                                    null=True, 
                                    blank=True
                                )
    max_seats           = models.IntegerField(null=True, blank=False, default=DEFAULT_MAX_SEATS)
    status              = models.CharField(
                                    max_length  = 64,
                                    choices     = CourseStatus.choices,
                                    default     = CourseStatus.INACTIVE,
                                    null        = False, 
                                    blank       = False
                                )
    category            = models.ForeignKey('Category', on_delete=models.CASCADE, null=False, blank=False)
    start_date          = models.DateTimeField(blank=True, null=True)
    end_date            = models.DateTimeField(blank=True, null=True)
    sessions            = models.IntegerField(null=True, blank=False, default=DEFAULT_SESSION_COUNT)
    duration            = models.IntegerField(null=True, blank=False, default=DEFAULT_SESSION_DURATION)

    class Meta:
        verbose_name    = "courses"
        db_table        = "courses"

    def __str__(self):
        return str(self.id)

    def __json__(self):
        return json.loads(serializers.serialize("json", [self]))[0]

    def soft_delete(self):
        self.deleted_at = datetime.datetime.now()


class Category(BaseModelMixin):
    id            = models.AutoField(primary_key=True)
    name          = models.CharField(max_length=128, null=True, blank=True, unique=True)
    description   = models.CharField(max_length=256, null=True, blank=True, unique=False)
    display_text  = models.CharField(max_length=128, null=True, blank=True, unique=False)
    icon          = models.CharField(max_length=256, null=True, blank=True)

    class Meta:
        verbose_name    = "categories"
        db_table        = "categories"

    def __str__(self):
        return str(self.id)

    def __json__(self):
        return json.loads(serializers.serialize("json", [self]))[0]

    def soft_delete(self):
        self.deleted_at = datetime.datetime.now()

