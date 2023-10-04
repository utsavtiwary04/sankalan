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
from catalogue.tests.fake_data import create_dummy_categories_courses
from catalogue.tasks import rebuild_search_index
from users.tests.fake_data import create_dummy_users

os.system("")
os.system("rm -rf db.sqlite3")
os.system("rm -rf migrations/")
os.system("python manage.py makemigrations")
os.system("python manage.py migrate")
os.system("python manage.py createsuperuser")



# Create 5 teachers, 10 Students, 4 categories (GPT)
## Create 25 Courses <> 5 Teachers (GPT)
### Index Search and test if it works
#### Register for course <> Success
##### Register for course <> Failure
###### Create 1 product segment with 2 products
####### Add to pricing to search
######## Create 1 category segment with 3 users
######### Create one global offer



## 1. Create Users
create_dummy_users()

## 2. Create categories and courses
create_dummy_categories_courses()

## 3. Index search and test if it works
rebuild_search_index()

## 4. Register a student for a course successfully

## 5. 