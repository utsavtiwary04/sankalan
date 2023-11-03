import pytz
from django.db import models
from datetime import datetime
from __common__.base_model import BaseModelMixin

class User(BaseModelMixin):
    name          = models.CharField(max_length=64, null=False, blank=False)
    phone         = models.CharField(max_length=20, null=False, blank=False)
    email         = models.CharField(max_length=200, null=True, blank=True)

    class Meta:
        verbose_name        = "users"
        verbose_name_plural = "users"

    ## Commonly used queries as methods
    @staticmethod
    def active_user(*args, **kwargs):
        base_query = kwargs.get("base_query")

        if base_query is None:
            base_query = User.objects

        if kwargs.get("user_id") is not None:
            base_query = base_query.filter(id=kwargs.get("user_id"))

        return base_query.filter(deleted_at=None).first()

    def __str__(self):
        return f"{self.id} {self.name} ({self.phone} | {self.email})"


class Channel(BaseModelMixin):
    name = models.CharField(max_length=64, null=False, blank=False)

    class Meta:
        verbose_name        = "channels"
        verbose_name_plural = "channels"

    @staticmethod
    def active_channel(*args, **kwargs):
        base_query = kwargs.get("base_query")

        if base_query is None:
            base_query = Channel.objects

        if kwargs.get("channel_id") is not None:
            base_query = base_query.filter(id=kwargs.get("channel_id"))

        if kwargs.get("channel_name") is not None:
            base_query = base_query.filter(name=kwargs.get("channel_name"))

        return base_query.filter(deleted_at=None).first()

    @staticmethod
    def active_channels():
        return Channel.objects.filter(deleted_at=None).all()

    def __str__(self):
        return f"{self.id} {self.name}"


class Comment(BaseModelMixin):
    text      = models.CharField(max_length=300, null=False, blank=False)
    user_ts   = models.BigIntegerField(null=False, blank=False)
    channel   = models.ForeignKey('Channel', on_delete=models.SET_NULL, null=True, blank=False)
    user      = models.ForeignKey('User', on_delete=models.SET_NULL, null=True, blank=False)

    class Meta:
        verbose_name        = "comments"
        verbose_name_plural = "comments"

    def to_json(self):
        return {
            "id":       self.id,
            "comment":  self.text,
            "time":     int(self.created_at.timestamp() * 1000),
            "username": self.user.name,
            "channel":  self.channel.name
        }

    @staticmethod
    def active_comment():
        return Comment.objects.filter(deleted_at=None)

    @staticmethod
    def active_comments():
        return Comment.active_comment.all()

    @staticmethod
    def comments_within(*args, **kwargs):
        if kwargs.get("base_query") is None:
            base_query = Comment.active_comment()

        if kwargs.get("start_ts"):
            start_date = datetime.fromtimestamp(start_ts, pytz.timezone("Asia/Kolkata"))
            base_query = base_query.filter(created_at__gte=start_date)

        if kwargs.get("end_ts"):
            end_date   = datetime.fromtimestamp(start_ts, pytz.timezone("Asia/Kolkata"))
            base_query = base_query.filter(created_at__lte=end_date)

        return base_query

    @staticmethod
    def recent_comments(*args, **kwargs):
        if kwargs.get("base_query") is None:
            base_query = Comment.active_comment()

        if kwargs.get("end_ts") is None:
            kwargs["end_ts"] = int(datetime.now().timestamp())

        if kwargs.get("start_ts") is None:
            kwargs["start_ts"] = int(datetime.now().timestamp()) - 84600 #default : last 1 day

        base_query = Comment.comments_within(kwargs)

        if kwargs.get("channel_id"):
            base_query = base_query.filter(channel_id=kwargs.get("channel_id"))

        return base_query.order_by('-created_at')[:kwargs.get("count", 10)]

    def __str__(self):
        return f"{self.id} {self.text} (By user {self.user.name} on channel {self.channel.name})"
