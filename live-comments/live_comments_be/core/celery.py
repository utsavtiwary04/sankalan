"""@@@
Configure your task queue here
@@@"""

import os

from celery import Celery, Task

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

app = Celery('live_comments_be')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')


app.autodiscover_tasks()

# @app.task(base=PeriodicTask, bind=True, ignore_result=True)
# def test_task(self):
#     print(f'Request: {self.request!r}')
