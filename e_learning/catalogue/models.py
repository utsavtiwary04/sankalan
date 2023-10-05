from django.db import models
from django.core import serializers
from __common__.base_model import BaseModelMixin

import json
import datetime

class CourseStatus(models.TextChoices):
    INACTIVE                = 'inactive'
    ACCEPTING_REGISTRATIONS = 'accepting_registrations'
    PAUSED_REGISTRATIONS    = 'paused_registrations'
    ENDED                   = 'ended'


class Category(BaseModelMixin):
    id            = models.AutoField(primary_key=True)
    name          = models.CharField(max_length=128, null=True, blank=True, unique=True)
    description   = models.CharField(max_length=256, null=True, blank=True, unique=False)
    display_text  = models.CharField(max_length=128, null=True, blank=True, unique=False)
    icon          = models.CharField(max_length=256, null=True, blank=True)

    class Meta:
        verbose_name        = "categories"
        verbose_name_plural = "categories"
        db_table            = "categories"

    @staticmethod
    def all():
        return Category.objects.filter(deleted_at=None).all()

    def __str__(self):
        return f"{self.id}. {self.name}"


class Course(BaseModelMixin):

    DEFAULT_SESSION_COUNT       = 10
    DEFAULT_SESSION_DURATION    = 90
    DEFAULT_MAX_SEATS           = 25
    DEFAULT_AMOUNT              = 99.0
    DEFAULT_HUMAN_READABLE_DATE = "%a, %-d %b %Y"

    # https://stackoverflow.com/questions/3936182/using-a-uuid-as-a-primary-key-in-django-models-generic-relations-impact TODO
    id                  = models.AutoField(primary_key=True)
    heading             = models.CharField(max_length=64, null=False, blank=False)
    description         = models.TextField(max_length=2000, null=True, blank=True)
    teacher             = models.ForeignKey('users.User', on_delete=models.SET_NULL, null=True, blank=False)
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
    category            = models.ForeignKey('Category', on_delete=models.SET_NULL, null=True, blank=False)
    start_date          = models.DateTimeField(blank=True, null=True)
    end_date            = models.DateTimeField(blank=True, null=True)
    sessions            = models.IntegerField(null=True, blank=False, default=DEFAULT_SESSION_COUNT)
    duration            = models.IntegerField(null=True, blank=False, default=DEFAULT_SESSION_DURATION)

    class Meta:
        verbose_name        = "courses"
        verbose_name_plural = "courses"
        db_table            = "courses"

    ## Commonly used queries as methods
    @staticmethod
    def active_course(course_id):
        return Course.objects.filter(id=course_id).filter(deleted_at=None).first()

    @staticmethod
    def all_courses_of_teacher(teacher_id):
        return Course.objects.filter(deleted_at=None).filter(teacher_id=teacher_id).all()

    @staticmethod
    def all():
        return Course.objects.filter(deleted_at=None).all()


    def __str__(self):
        return f"""
            {self.id}. {self.heading} by {self.teacher.full_name() if self.teacher else '-'} 
            ({self.currency} {self.amount} | 
            {self.max_seats} seats | 
            {self.start_date.strftime("%a, %-d %b %Y")} to {self.end_date.strftime("%a, %-d %b %Y")})
            """

    def to_json(self):
        json_object = json.loads(serializers.serialize("json", [self]))[0]

        return { 
            **{ "id" : json_object.pop("pk") },
            **dict(json_object["fields"]) 
        }

    def _start_date(self, date_format=DEFAULT_HUMAN_READABLE_DATE):
        return self.start_date.strftime(date_format)

    def _end_date(self, date_format=DEFAULT_HUMAN_READABLE_DATE):
        return self.start_date.strftime(date_format)

    def soft_delete(self):
        self.deleted_at = datetime.datetime.now()

    def has_ended(self):
        return self.end_date >= datetime.datetime.today().astimezone()

    def is_accepting_registrations(self):
        return self.status == "ACCEPTING_REGISTRATIONS"


class CourseRegistration(BaseModelMixin):

    student = models.ForeignKey('users.User', on_delete=models.SET_NULL, null=True, blank=False)
    course  = models.ForeignKey('Course', on_delete=models.SET_NULL, null=True, blank=False)
    start   = models.DateTimeField(blank=True, null=True)
    end     = models.DateTimeField(blank=True, null=True)

    class Meta:
        verbose_name        = "course_registrations"
        verbose_name_plural = "course_registrations"
        db_table            = "course_registrations"

    ## Commonly used queries as methods
    @staticmethod
    def registrations_of_course(course_id: int):
        return CourseRegistration.objects.filter(course_id=course_id).filter(deleted_at=None).all()

    @staticmethod
    def registrations_of_student(student_id: int):
        return CourseRegistration.objects.filter(student_id=student_id).filter(deleted_at=None).all()

