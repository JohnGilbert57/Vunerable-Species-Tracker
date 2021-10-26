"""Renders our page forms and views"""
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views import generic
from django.views.generic import TemplateView
from django.contrib.auth.models import User
import datetime
from .forms import NewUserForm
from django.utils import timezone

"""This function renders our create account form"""
def new_user_form(response):
    if response.method == "POST":
        form = NewUserForm(response.POST)
        if form.is_valid():
            form.save()
            return redirect('/login')
    else:
        form = NewUserForm()
    context = {
        'form': form
    }
    return render(response, './newUser/new_user.html', context)


"""Landing page Response Return"""
def landingpage(response):
    return render(response, './landingpage/landingpage.html')

"""if the base url is accessed redirect them to login"""
def baseUrl(response):
    return redirect('/login')

# Class used for Chart/Sprite

