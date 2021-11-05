"""Renders our page forms and views"""
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views import generic
from django.views.generic import TemplateView
from django.contrib.auth.models import User
import datetime
from django.utils import timezone
from django.http.request import HttpRequest
from myapp.database import *


"""Landing page Response Return"""
def landingpage(response):
    if response.user.is_authenticated:
        return render(response, './landingpage/landingpage.html')
    return redirect('/login')

"""if the base url is accessed redirect them to login"""
def baseUrl(response):
    return redirect('/login')

def managePage(response):
    if response.user.is_authenticated:
        species = db_query("select common_name, scientific_name, region_name, status_name, group_name from species s,region r,species_group sg,status st where s.status_id=st.status_id and s.region_id=r.region_id and s.group_id=sg.group_id");
        context = {
            'species': species
        }
        return render(response,'./manage/manage.html',context)
    return redirect('/login')

def educationList(response):
    if response.user.is_authenticated:
        return render(response, './education/educationList.html')
    return redirect('/login')
