from django.shortcuts import render
from django.http import HttpResponse

def health(request):
    return HttpResponse("Health Check :: Users")