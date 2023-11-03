find . -name '*.pyc' -type f -delete && find . | grep -E "(/__pycache__$|\.pyc$|\.pyo$)" | xargs rm -rf
python manage.py runserver
python -m celery -A core worker --loglevel=info --concurrency=2
yarn dev
yarn server
python -m celery -A e_learning flower

celery-beat / run migrations
https://www.nickmccullum.com/celery-django-periodic-tasks/#using-django-celery-beat