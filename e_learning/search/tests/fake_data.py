import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Musical.settings")
import django
django.setup()
from faker import factory, Faker
from search.models import *
from model_bakery.recipe import Course

myfake = Faker()

for k in range(50):
	singers = Recipe(Singers,
		name = myfake.name(),
		address = myfake.address(),
	created_prof = myfake.future_datetime(end_date="+30d", tzinfo=None),)
