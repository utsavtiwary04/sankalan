import django
django.setup()
import random
from itertools import cycle
# from model_bakery import baker
# from model_bakery.recipe import Recipe

# from search.models import Course, CourseStatus, Category

# category = Recipe(
#     Category,
#     name         = cycle(["Baking", "Art", "Fitness", "Gardening"]),
#     description  = "Another interesting category",
#     display_text = "Baking",
#     icon         = "https://images.unsplash.com/photo-1695095737430-78fD%3D&auto=format&fit=crop&w=2670&q=80"
# )

# course = Recipe(
#     Course,
#     heading     = "Learn how to bake",
#     description = "This is a course that teaches you how to bake. Total 5 lessons only",
#     amount      = cycle([random.randint(999, 4999) for i in range(100)]),
#     currency    = cycle(["INR"]),
#     max_seats   = cycle([random.randint(5, 50) for i in range(20)]),
#     status      = cycle(CourseStatus.names),
#     discount_currency = cycle(["INR"])
#     # category=
# )



# ##############################################################

# import factory
# import factory.fuzzy

# class CourseFactory(factory.django.DjangoModelFactory):

#     class Meta: 
#         model = Course

#     heading     = factory.Faker("name")
#     description = factory.Faker("sentence")
#     amount      = factory.fuzzy.FuzzyChoice(choices=[random.randint(999, 4999) for i in range(100)])
#     currency    = factory.fuzzy.FuzzyChoice(choices=["INR"])
#     max_seats   = factory.fuzzy.FuzzyChoice(choices=[random.randint(5, 50) for i in range(20)])
#     status      = factory.fuzzy.FuzzyChoice(choices=CourseStatus.names)
#     discount_currency = factory.fuzzy.FuzzyChoice(choices=["INR"])
#     category = None


# courses = CourseFactory.create_batch(10)





######################## GPT Powered Dummy Data #######################

"""
Prompt:
generate the details of 50 online courses in the domain of music, art or dance with the following fields and constraints with each of them
1. heading in maximum 50 characters
2. brief curriculum of the course in 200 characters
3. price of the course ranging anywhere between 999 to 7999
4. currency of the course which is always "INR"
5. start date of the course which is any date from 1st Jan 2020 to 1st Jan 2026 and in the format "dd-mm-yyyy"
6. end date of the course which is any date greater than start date with a maximum of 2 months from start date and in the format "dd-mm-yyyy"
7. Total number of sessions ranging from 5 to 25 classes
8. duration of the session should be between 45 to 90 mins in steps of 15 mins
9. category which is one of the following "music", "art" or "dance" depending upon the heading
10. teacher_id should be an integer from 1 to 10 with the same teacher_id for a category
11. max_seats should be an integer between 5 and 50 in steps of 5

The output should be a list of json with the following keys - "heading", "description", "price", "currency", "start_date", "end_date", "sessions", "duration", "category", Make sure the examples are realistic. Some of the courses'  start_date end_date should be ahead of 10th October, 2025.
Some of the courses should be ongoing while some should have ended.
"""

"""
Prompt:
Generate 10 fake user data for testing consisting of name, age and gender as a list of json. The age should be between 25 and 45. The names should be a mix of indian or American names.
"""



from catalogue.models import Course,Category
from users.tests.fake_data import create_dummy_users
import datetime



def create_dummy_categories_courses():
    fake_categories_list = []
    fake_course_list     = []

    with open('dummy_categories_data.json') as category_data_file:
        fake_categories_list = json.load(category_data_file)

    with open('dummy_course_data.json') as course_data_file:
        fake_course_list = json.load(course_data_file)

    for cat in fake_categories_list:
        Category.objects.create(**cat)

    for course in fake_course_list:
        course["start_date"] = datetime.datetime.strptime(course["start_date"], "%d-%m-%Y").astimezone()
        course["end_date"]   = datetime.datetime.strptime(course["end_date"], "%d-%m-%Y").astimezone()
        Course.objects.create(**course)




