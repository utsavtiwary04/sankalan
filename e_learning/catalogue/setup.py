############## MODULE SETUP FILE ####################

#### PRE-REQUISITES (running locally on default ports):
# - Django server
# - Elasticsearch 8.xx and above
# - Redis
# - Celery



#### WHAT DOES THIS FILE DO ?
# - Runs DB Migrations in a local sqlite instance
# - Enters dummy data in models
# - Sets up elasticsearch index
# - Indexes elasticsearch with the data from sqlite
# - Triggers change in data in sqlite
# - Re-indexes one document to check if celery + redis is working fine


import os
import subprocess

os.system("")
os.system("rm -rf db.sqlite3")
os.system("rm -rf migrations/")
os.system("python manage.py makemigrations")
os.system("python manage.py migrate")
os.system("python manage.py createsuperuser")

# subprocess.Popen