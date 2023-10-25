import json
from django.core import serializers
from django.db import models


class BaseManager(models.Manager):
    use_in_migrations = True

    def get_queryset(self):
        return super().get_queryset().filter(deleted_at=None)


class TimestampMixin(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        abstract = True


class BaseModelMixin(TimestampMixin):
    meta    = models.JSONField(default=dict, blank=True, null=True)
    objects = BaseManager()

    class Meta:
        abstract = True

    def to_json(self):
        json_object = json.loads(serializers.serialize("json", [self]))[0]

        return {
            **{ "id" : json_object.pop("pk") },
            **dict(json_object["fields"])
        }

    def soft_delete(self):
        self.deleted_at = datetime.datetime.now()
