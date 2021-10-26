"""serves our urls to the browser"""
from django.urls import path, include
from . import views
from .views import new_user_form, landingpage

urlpatterns = [
    path('', views.baseUrl),
    path('', include("django.contrib.auth.urls")),
    path('createaccount/', new_user_form, name = "register"),
    path('landingpage/', landingpage),
   # path('hobbyview/', HobbyChartView.as_view(), name='home'),
   # path('hobbyview/addtime', hobby_time_form, name = 'addtime')
]
