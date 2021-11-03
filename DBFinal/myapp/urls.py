"""serves our urls to the browser"""
from django.urls import path, include
from . import views
from .views import landingpage, managePage, educationList

urlpatterns = [
    path('', views.baseUrl),
    path('', include("django.contrib.auth.urls")),
    path('landingpage/', landingpage),
    path('manage/', managePage),
    path('education/', educationList)
]
