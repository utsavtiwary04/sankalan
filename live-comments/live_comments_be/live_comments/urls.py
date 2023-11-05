from django.urls import path
from . import views

urlpatterns = [
    path("health", views.health, name="health"),
    path("channels/active", views.all_active_channels, name="active_channels"),
    path("comments/new", views.new, name="new_comments"),
    path("comments/past", views.past, name="past_comments")
]