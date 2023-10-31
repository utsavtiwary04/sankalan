from django.urls import path
from . import views

urlpatterns = [
    path("health", views.health, name="health"),
    path("comments/new", views.new, name="new"),
    path("comments/past", views.past, name="past")
]