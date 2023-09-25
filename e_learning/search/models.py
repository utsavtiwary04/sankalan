from django.db import models
from django.utils.translation import gettext_lazy as _
from __common__.base_model import BaseModelMixin
from django.contrib.postgres.fields import ArrayField

import uuid
import datetime

def generate_course_code():
    return f"CPN{str(uuid.uuid4())[:8]}"

class CourseStatus(models.TextChoices):
    INACTIVE                = 'inactive'
    ACCEPTING_REGISTRATIONS = 'accepting_registrations'
    PAUSED_REGISTRATIONS    = 'paused_registrations'
    ENDED                   = 'ended'

class Course(BaseModelMixin):
	# https://stackoverflow.com/questions/3936182/using-a-uuid-as-a-primary-key-in-django-models-generic-relations-impact
    id                  = models.AutoField(primary_key=True)
    heading		        = models.CharField(max_length=64, null=False, blank=False)
    description         = models.TextField(max_length=2000, null=True, blank=True)     
    schedule     		= ArrayField(models.IntegerField(null=True, blank=True,default=None),default=list,blank=False,null=False) ## NEEDS FIXING
    teacher_id	       	= models.CharField(max_length=64, null=False, blank=False)  #unique true
    amount       		= models.DecimalField(
                                    decimal_places=2, 
                                    default=0.0, 
                                    max_digits=8, 
                                    null=False, 
                                    blank=False
                                )
    currency 		    = models.CharField(
                                    max_length=20, 
                                    default="INR", 
                                    null=True, 
                                    blank=True
                                )
    max_seats      		= models.IntegerField(null=True, blank=False, default=25)
    status				= models.CharField(
                                    max_length  = 64,
                                    choices     = CourseStatus.choices,
                                    default     = CourseStatus.INACTIVE,
                                    null        = False, 
                                    blank       = False
                                )
    discount_currency   = models.CharField(
                                    max_length=20, 
                                    default="INR", 
                                    null=True, 
                                    blank=True
                                )
    category            = ArrayField(models.IntegerField(null=True, blank=False, default=25),
    								default=list,
    								blank=False,
    								null=False
    							)

    def __str__(self):
        return str(self.id)

    def soft_delete(self):
        self.deleted_at = datetime.datetime.now()

    class Meta:
        verbose_name    = "courses"
        db_table        = "courses"

class Category(BaseModelMixin):
    id            = models.AutoField(primary_key=True)
    name          = models.CharField(max_length=128, null=True, blank=True, unique=True)
    description   = models.CharField(max_length=256, null=True, blank=True, unique=False)
    display_text  = models.CharField(max_length=128, null=True, blank=True, unique=False)
    icon          = models.CharField(max_length=256, null=True, blank=True)

    class Meta:
        verbose_name    = "categories"
        db_table        = "categories"
