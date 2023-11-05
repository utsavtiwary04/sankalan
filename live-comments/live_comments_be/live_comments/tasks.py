import socketio
from datetime import datetime, timedelta
from celery import shared_task
from celery.signals import task_failure

from .models import User, Comment, Channel
from .exceptions import EntityNotFound

@shared_task(name="live_comments.save_new_comment",
             autoretry_for=(Exception,),
             retry_kwargs={'max_retries': 2, 'countdown': 1})
def save_new_comment(data: dict):
    user    = User.active_user(data["user_id"])
    channel = Channel.active_channel(channel_id=data["channel_id"])

    if not user:
        raise EntityNotFound(User.__name__, data["user_id"])

    if not channel:
        raise EntityNotFound(Channel.__name__, data["channel_id"])

    new_comment = Comment(user=user,
                          channel=channel,
                          text=data["comment"],
                          user_ts=data["user_ts"])
    new_comment.save()

@task_failure.connect(sender=save_new_comment)
def task_failure_notifier(sender=None, **kwargs):
    print("From task_failure_notifier ==> Task failed ")
    print(kwargs)



@shared_task(name="live_comments.publisher",
             autoretry_for=(Exception,),
             retry_kwargs={'max_retries': 2, 'countdown': 1})
def publisher(timedelta=60):
    ## Read the most recent messages from the DB in the last one minute
    now           = int(datetime.now().timestamp())
    channels      = Channel.active_channels()
    timedelta     = 60 or timedelta #seconds
    message_count = 10

    if len(channels) > 0:
        sio = socketio.SimpleClient()
        sio.connect('http://localhost:8001')

        for channel in channels:
            print(f"EMITTING FOR {len(channels)} channels")
            comments = Comment.recent_comments(count=message_count, start=now-timedelta, end=now, channel_id=channel.id)

            if len(comments) > 0:
                sio.emit('message', {
                                        "channel_id"   : channel.id,
                                        "channel_name" : channel.name,
                                        "messages"     : [c.to_json() for c in comments]
                                    })
        sio.disconnect()
            #   message => {
            #     'id': 34,
            #     'comment': 'This is a stream',
            #     'time': 1698739491012,
            #     'username': 'Utsav Tiwary',
            #     'channel': 'foodandtravel'
            #   },
