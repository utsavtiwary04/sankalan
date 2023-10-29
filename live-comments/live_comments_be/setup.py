find . -name '*.pyc' -type f -delete && find . | grep -E "(/__pycache__$|\.pyc$|\.pyo$)" | xargs rm -rf
python manage.py runserver
python -m celery -A core worker --loglevel=info --concurrency=2
yarn dev
yarn server
python -m celery -A e_learning flower
