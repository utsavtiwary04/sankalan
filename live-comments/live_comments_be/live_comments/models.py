from django.db import models
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
    user_ts   = models.IntegerField(null=False, blank=False)
    channel   = models.ForeignKey('Channel', on_delete=models.SET_NULL, null=True, blank=False)
    user      = models.ForeignKey('User', on_delete=models.SET_NULL, null=True, blank=False)

    class Meta:
        verbose_name        = "comments"
        verbose_name_plural = "comments"

    @staticmethod
    def comments_within(start_ts, end_ts):
        start_date, end_date = datetime.datetime.from_timestamp(start_ts),\
                                datetime.datetime.from_timestamp(end_ts) 
        return Comment.objects.filter(created_at__gte=start_ts).filter(created_at__lte=end_ts).all()

    def __str__(self):
        return f"{self.id} {self.text} (By user {self.user.name} on channel {self.channel.name})"
