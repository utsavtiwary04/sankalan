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
    def active_user(user_id):
        return User.objects.filter(id=user_id).filter(deleted_at=None).first()

    def __str__(self):
        return f"{self.id} {self.name} ({self.phone} | {self.email})"


class Channel(BaseModelMixin):
    name = models.CharField(max_length=64, null=False, blank=False)

    class Meta:
        verbose_name        = "channels"
        verbose_name_plural = "channels"

    ## Commonly used queries as methods
    @staticmethod
    def active_channel_by_id(channel_id):
        return Channel.objects.filter(id=channel_id).filter(deleted_at=None).first()

    @staticmethod
    def active_channel_by_name(channel_name):
        return Channel.objects.filter(name=channel_name).filter(deleted_at=None).first()

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
            "username": self.user.name,
            "channel":  self.channel.name
        }

    @staticmethod
    def active_comments():
        return Comment.objects.filter(deleted_at=None)

    @staticmethod
    def comments_within(base_query, start_ts, end_ts):
        if base_query is None:
            base_query = Comment.active_comments()

        start_date, end_date = datetime.fromtimestamp(start_ts, pytz.timezone("Asia/Kolkata")),\
                                datetime.fromtimestamp(end_ts, pytz.timezone("Asia/Kolkata")) 
        return base_query.filter(created_at__gte=start_date).filter(created_at__lte=end_date)

    @staticmethod
    def recent_comments(base_query=None, count=10, start_ts=None, end_ts=None, channel_id=None):
        if base_query is None:
            base_query = Comment.active_comments()

        if end_ts is None:
            end_ts = int(datetime.now().timestamp())

        if start_ts is None:
            start_ts = int(datetime.now().timestamp()) - 60 #seconds

        base_query = Comment.comments_within(base_query, start_ts, end_ts)

        if channel_id is not None:
            base_query = base_query.filter(channel_id=channel_id)

        return base_query.order_by('-created_at')[:count]

    def __str__(self):
        return f"{self.id} {self.text} (By user {self.user.name} on channel {self.channel.name})"
