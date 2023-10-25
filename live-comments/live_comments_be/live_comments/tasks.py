from celery import shared_task

@shared_task(autoretry_for=(Exception,), retry_kwargs={'max_retries': 3, 'countdown': 2})
def test_task():
    print("hello task")