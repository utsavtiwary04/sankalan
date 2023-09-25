from celery import Celery

app = Celery('tasky', broker='redis://127.0.0.1:6379/0', backend='redis://127.0.0.1:6379/0')

@app.task
def add(x, y):
    return x + y