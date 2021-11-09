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
from .forms import AddSpeciesForm, EditSpeciesForm
from .models import Species


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
        if response.method == "POST" and 'Create' in response.POST:
            form = AddSpeciesForm(response.POST)
            if form.is_valid():
                commonName = form.cleaned_data.get('commonName')
                scientificName = form.cleaned_data.get('scientificName')
                region = form.cleaned_data.get('region')
                conservationStatus = form.cleaned_data.get('conservationStatus')
                group = form.cleaned_data.get('group')
                newId = db_query('SELECT MAX(SPECIES_ID) FROM SPECIES')
                newId = max(newId)[0] + 1
                db_query('INSERT INTO SPECIES (SPECIES_ID, COMMON_NAME, SCIENTIFIC_NAME, REGION_ID, STATUS_ID, GROUP_ID) VALUES(%s, %s, %s, %s, %s, %s)', [newId, commonName, scientificName, region, conservationStatus, group])
        if response.method == "POST" and 'update' in response.POST:
            form = EditSpeciesForm(response.POST)
            if form.is_valid():
                sId = response.POST.get('update')
                commonName = form.cleaned_data.get("cName")
                scientificName = form.cleaned_data.get('sName')
                region = form.cleaned_data.get('reg')
                conservationStatus = form.cleaned_data.get('cStatus')
                group = form.cleaned_data.get('grp')
                db_query('UPDATE SPECIES SET COMMON_NAME =  %s, SCIENTIFIC_NAME = %s, REGION_ID = %s, STATUS_ID = %s, GROUP_ID =%s WHERE SPECIES_ID = %s', [commonName, scientificName, region, conservationStatus, group, sId])
        if response.method == "POST" and 'delete' in response.POST:
            delete_key = response.POST.get('delete')
            db_query('DELETE FROM SPECIES WHERE SPECIES_ID = %s', [delete_key])
        form = AddSpeciesForm()
        form2 = EditSpeciesForm()
        species = db_query("select species_id, common_name, scientific_name, region_name, status_name, group_name from species s,region r,species_group sg,status st where s.status_id=st.status_id and s.region_id=r.region_id and s.group_id=sg.group_id")
        context = {
            'species': species,
            'form': form,
            'form2': form2
        }
        return render(response,'./manage/manage.html',context)
    return redirect('/login')

def educationList(response):
    if response.user.is_authenticated:
        mammals = db_query("select species_id, common_name, scientific_name, region_name, status_name, group_name from species s,region r,species_group sg,status st where s.status_id=st.status_id and s.region_id=r.region_id and s.group_id=sg.group_id and sg.group_name = 'Mammals'")
        context = {
            'mammals': mammals
        }
        return render(response, './education/educationList.html', context)
    return redirect('/login')

def manageRegion(response):
    if response.user.is_authenticated:
        return render(response, './manage/manageregions.html')
    return redirect('/login')

def manageGroups(response):
    if response.user.is_authenticated:
        return render(response, './manage/managegroups.html')
    return redirect('/login')

def manageStatuses(response):
    if response.user.is_authenticated:
        return render(response, './manage/managestatuses.html')
    return redirect('/login')
