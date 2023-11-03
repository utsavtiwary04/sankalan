import traceback
from django.shortcuts import render
from django.http import HttpResponse

from rest_framework.response import Response
from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import JSONParser
from rest_framework import serializers

from .service import new_comment, past_comments
from .exceptions import EntityNotFound, GenericAPIException



def health(request):
    return HttpResponse("Health Check :: Live Comments")

@api_view(['POST'])
@parser_classes([JSONParser])
def new(request, format=None):
    
    class NewCommentRequest(serializers.Serializer):
        user_id    = serializers.IntegerField()
        channel_id = serializers.IntegerField()
        comment    = serializers.CharField(max_length=50)
        user_ts    = serializers.IntegerField()

    try:
        request = NewCommentRequest(data=request.data)

        if not request.is_valid():
            errors = {key :" ".join([str(e) for e in error_list]) for key, error_list in request.errors.items()}
            return Response(status=400, data={'data': request.errors, 'success': False})

        return Response(status=201, data={'data': new_comment(request.data), 'success': True})

    except Exception as e:
        traceback.print_exception(e)
        return Response(status=500, data={'data': "Something broke. Our fault - not yours :(", 'success': False})

@api_view(['GET'])
@parser_classes([JSONParser])
def past(request, format=None):
    
    class PastCommentsRequest(serializers.Serializer):
        count      = serializers.IntegerField()
        channel_id = serializers.IntegerField()

    try:
        request  = PastCommentsRequest(data=request.query_params.dict())
        if not request.is_valid():
            errors = {key :" ".join([str(e) for e in error_list]) for key, error_list in request.errors.items()}
            return Response(status=400, data={'data': request.errors, 'success': False})

        comments = past_comments(channel_id=request.data["channel_id"], count=request.data["count"])

        return Response(status=200, data={'data': comments, 'success': True})

    except EntityNotFound as e:
        return Response(status=400, data={'data': str(e), 'success': False})

    except Exception as e:
        traceback.print_exception(e)
        return Response(status=500, data={'data': "Something broke. Our fault - not yours :(", 'success': False})
