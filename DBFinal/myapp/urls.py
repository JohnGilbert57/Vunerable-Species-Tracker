"""serves our urls to the browser"""
from django.urls import path, include
from . import views
from .views import landingpage, managePage, educationList, manageGroups, manageRegion, manageStatuses

urlpatterns = [
    path('', views.baseUrl),
    path('', include("django.contrib.auth.urls")),
    path('landingpage/', landingpage),
    path('landingpage/manage/', managePage),
    path('landingpage/manage/regions/', manageRegion),
    path('landingpage/manage/groups', manageGroups),
    path('landingpage/manage/statuses', manageStatuses),
    path('landingpage/education/', educationList)
]
