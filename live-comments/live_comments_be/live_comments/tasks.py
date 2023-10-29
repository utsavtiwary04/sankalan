from .models import User, Comment, Channel
from .exceptions import EntityNotFound
from celery import shared_task, Task
from celery.signals import task_failure
from celery.contrib import rdb

@shared_task(name="live_comments.save_comment",
            autoretry_for=(Exception,),
            retry_kwargs={'max_retries': 2, 'countdown': 1})
def save_comment(data: dict):
    user    = User.active_user(data["user_id"])
    channel = Channel.active_channel_by_id(data["channel_id"])

    if not user:
        raise EntityNotFound(data["user_id"], User.__name__)

    if not channel:
        raise EntityNotFound(data["channel_id"], Channel.__name__)


@task_failure.connect(sender=save_comment)
def task_failure_notifier(sender=None, **kwargs):
    print("From task_failure_notifier ==> Task failed ")
    print(kwargs)
    # rdb.set_trace()
