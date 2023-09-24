from django.shortcuts import render
from django.http import HttpResponse


def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")

# API

# search + filter + sort + paginate
# ----------------------------------
# /v1/courses/search?term=baking&filter=&sort=&min_price=899&max_price=1999&limit=10&offset=100


# categories with count
# ---------------------
# v1/courses/categories/<category_name>


# bestsellers
# -----------
# v1/courses/bestsellers








