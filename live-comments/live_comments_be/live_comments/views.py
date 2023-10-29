from django.shortcuts import render
from django.http import HttpResponse

from rest_framework.response import Response
from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import JSONParser
from rest_framework import serializers

from .service import new_comment

class NewComment(serializers.Serializer):
    user_id    = serializers.IntegerField()
    channel_id = serializers.IntegerField()
    comment    = serializers.CharField(max_length=50)

def health(request):
    return HttpResponse("Health Check :: Live Comments")

@api_view(['POST'])
@parser_classes([JSONParser])
def comment(request, format=None):
    try:
        request = NewComment(data=request.data)

        if not request.is_valid():
            errors = {key :" ".join([str(e) for e in error_list]) for key, error_list in request.errors.items()}
            return Response(status=400, data={'data': request.errors, 'success': False})

        return Response(status=200, data={'data': new_comment(request.data), 'success': True})

    except Exception as e:
        return Response(status=500, data={'data': str(e), 'success': False})