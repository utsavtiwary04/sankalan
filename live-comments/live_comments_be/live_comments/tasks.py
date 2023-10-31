import socketio
from datetime import datetime, timedelta
from celery import shared_task
from celery.signals import task_failure

from .models import User, Comment, Channel
from .exceptions import EntityNotFound

@shared_task(name="live_comments.save_comment",
            autoretry_for=(Exception,),
            retry_kwargs={'max_retries': 2, 'countdown': 1})
def save_comment(data: dict):
    user    = User.active_user(data["user_id"])
    channel = Channel.active_channel_by_id(data["channel_id"])

    if not user:
        raise EntityNotFound(User.__name__, data["user_id"])

    if not channel:
        raise EntityNotFound(Channel.__name__, data["channel_id"])

    new_comment = Comment(user=user,
                          channel=channel,
                          text=data["comment"],
                          user_ts=data["user_ts"])
    new_comment.save()
    # publisher(f"{user.name} said '{new_comment.text}'")


@task_failure.connect(sender=save_comment)
def task_failure_notifier(sender=None, **kwargs):
    print("From task_failure_notifier ==> Task failed ")
    print(kwargs)
    # rdb.set_trace()


def publisher(message):
    sio = socketio.SimpleClient()
    sio.connect('http://localhost:8001')

    ## Read the most recent messages from the DB in the last one minute
    now      = int(datetime.now().timestamp())
    channels = Channel.active_channels()
    for channel in active_channels:
        comments = Comment.recent_comments(count=10, start=now-60, end=now, channel_id=channel.id)

        if len(comments) > 0:
            message_payload = [
                {
                    "username": comment.user.name,
                    "comment": comment.text,
                    "time": comment.user_ts
                } for comment in comments
            ]
            sio.emit('message', { "messages" : message_payload})
