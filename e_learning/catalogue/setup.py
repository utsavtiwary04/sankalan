############## MODULE SETUP FILE ####################

#### PRE-REQUISITES (running locally on default ports):
# - Django server
# - Elasticsearch 8.xx and above
# - Redis
# - Celery


#### WHAT DOES THIS FILE DO ?
# - Runs DB Migrations in a local sqlite instance
## - Enters dummy data in models
### - Sets up elasticsearch index
#### - Indexes elasticsearch with the data from sqlite
##### - Triggers change in data in sqlite
###### - Re-indexes one document to check if celery + redis is working fine


import os
import time
import django
django.setup()
from catalogue.tests.fake_data import create_dummy_categories_courses
from catalogue.pricing.models import Campaign, ProductSegment, UserSegment
from catalogue.search.tasks import rebuild_search_index
from users.tests.fake_data import create_dummy_users

print("\n 💿 CLEANING DB & CREATING SUPER USER \n")
time.sleep(2.5)

os.system("")
os.system("rm -rf db.sqlite3")
os.system("""find . -path "*migrations*" -not -regex ".*__init__.py" -a -not -regex ".*migrations" | xargs rm -rf""")
os.system("python manage.py makemigrations")
os.system("python manage.py migrate")
os.system("python manage.py createsuperuser")

#### Register for course <> Success
##### Register for course <> Failure
###### Create 1 product segment with 2 products
####### Add to pricing to search
######## Create 1 category segment with 3 users
######### Create one global offer



## 1. Create Users
print("\n 👨🏼‍🦰 CREATING DUMMY USERS \n")
time.sleep(2)
create_dummy_users()

## 2. Create categories and courses
print("\n 📚 CREATING DUMMY CATEGORIES AND COURSES \n")
time.sleep(2)
create_dummy_categories_courses()

## 3. Index search and test if it works
print("\n 🔎 BUILDING SEARCH INDEX \n")
time.sleep(2)
rebuild_search_index.delay()

print("\n 🔑 STARTING SERVER !\n")
os.system("python manage.py runserver")

print("\n 🚀 WE ARE READY !\n")
print("Click here - http://localhost:8000/catalogue/search/?keyword=music&limit=15 \n")





## 4. Register a student for a course successfully

## 5. more more
