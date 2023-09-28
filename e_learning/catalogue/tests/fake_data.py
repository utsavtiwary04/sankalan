import django
django.setup()
import random
from itertools import cycle
from model_bakery import baker
from model_bakery.recipe import Recipe

from search.models import Course, CourseStatus, Category

category = Recipe(
    Category,
    name         = cycle(["Baking", "Art", "Fitness", "Gardening"]),
    description  = "Another interesting category",
    display_text = "Baking",
    icon         = "https://images.unsplash.com/photo-1695095737430-78fD%3D&auto=format&fit=crop&w=2670&q=80"
)

course = Recipe(
    Course,
    heading     = "Learn how to bake",
    description = "This is a course that teaches you how to bake. Total 5 lessons only",
    amount      = cycle([random.randint(999, 4999) for i in range(100)]),
    currency    = cycle(["INR"]),
    max_seats   = cycle([random.randint(5, 50) for i in range(20)]),
    status      = cycle(CourseStatus.names),
    discount_currency = cycle(["INR"])
    # category=
)



##############################################################

import factory
import factory.fuzzy

class CourseFactory(factory.django.DjangoModelFactory):

    class Meta: 
        model = Course

    heading     = factory.Faker("name")
    description = factory.Faker("sentence")
    amount      = factory.fuzzy.FuzzyChoice(choices=[random.randint(999, 4999) for i in range(100)])
    currency    = factory.fuzzy.FuzzyChoice(choices=["INR"])
    max_seats   = factory.fuzzy.FuzzyChoice(choices=[random.randint(5, 50) for i in range(20)])
    status      = factory.fuzzy.FuzzyChoice(choices=CourseStatus.names)
    discount_currency = factory.fuzzy.FuzzyChoice(choices=["INR"])
    category = None


courses = CourseFactory.create_batch(10)
