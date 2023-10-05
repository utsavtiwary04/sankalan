from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.response import Response
from rest_framework.views import APIView

from rest_framework import serializers
from rest_framework.decorators import api_view
from rest_framework.decorators import parser_classes
from rest_framework.parsers import JSONParser

from .search.service import search_catalogue
from .search.tasks import rebuild_search_index

class SearchRequest(serializers.Serializer):
    term   = serializers.CharField(max_length=200)
    filter = serializers.CharField(max_length=50)
    sort   = serializers.CharField(max_length=50)
    limit  = serializers.IntegerField()
    offset = serializers.IntegerField()



def health(request):
    rebuild_search_index.delay()
    return HttpResponse("You know, for search (init full reindex...)")


@api_view(['GET'])
@parser_classes([JSONParser])
def search(request, format=None):
    params = request.query_params.dict()
    data   = search_catalogue(params)

    return Response(status=200, data={'data': data, 'success': True})



## TODO : Add Structlog ##

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








