"""Created forms that will be called to pass forms to the html"""
# Johnny Gilbert
# Ohio University
# the format for the user login; creates the objects basesd upon the models and sets the data
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import *
from myapp.database import *

class AddSpeciesForm(forms.ModelForm):
    
    """creating a new hobby"""
    class Meta:
        model = AddSpecies
        fields = [
            'commonName',
            'scientificName',
            'region',
            'conservationStatus',
            'group'
        ]
        REGION = to_tuples(db_query('select region_id,region_name from region'))
        STATUS = to_tuples(db_query('select status_id,status_name from status'))
        GROUP = to_tuples(db_query('select group_id,group_name from species_group'))
        widgets = {
            'commonName': forms.TextInput(attrs={"class": "form-control"}),
            'scientificName': forms.TextInput(attrs={"class": "form-control"}),
            'region': forms.Select(attrs={"class": "form-control"}, choices = REGION),
            'conservationStatus': forms.Select(attrs={"class": "form-control"}, choices = STATUS),
            'group': forms.Select(attrs={"class": "form-control"}, choices = GROUP)
        }
        labels = {
            'commonName': 'Common Name: ',
            'scientificName': 'Scientific Name: ',
            'region': 'Region: ',
            'conservationStatus': 'Conservation Status: ',
            'group': 'Group: '
        }

class EditSpeciesForm(forms.ModelForm):
    """creating a new hobby"""
    class Meta:
        model = EditSpecies
        fields = [
            'cName',
            'sName',
            'reg',
            'cStatus',
            'grp'
        ]
        REGION = to_tuples(db_query('select region_id,region_name from region'))
        STATUS = to_tuples(db_query('select status_id,status_name from status'))
        GROUP = to_tuples(db_query('select group_id,group_name from species_group'))
        widgets = {
            'cName': forms.TextInput(attrs={"class": "form-control"}),
            'sName': forms.TextInput(attrs={"class": "form-control"}),
            'reg': forms.Select(attrs={"class": "form-control"}, choices = REGION),
            'cStatus': forms.Select(attrs={"class": "form-control"}, choices = STATUS),
            'grp': forms.Select(attrs={"class": "form-control"}, choices = GROUP)
        }
        labels = {
            'cName': 'Common Name: ',
            'sName': 'Scientific Name: ',
            'reg': 'Region: ',
            'cStatus': 'Conservation Status: ',
            'grp': 'Group: '
        }

class AddRegionForm(forms.ModelForm):
    class Meta:
        model = AddRegion
        fields = [
            'region'
        ]
        widgets = {
            'region': forms.TextInput(attrs={"class": "form-control"}),
        }
        labels = {
            'region': 'Region: '
        }

class EditRegionForm(forms.ModelForm):
    class Meta:
        model = EditRegion
        fields = [
            'reg'
        ]
        widgets = {
            'reg': forms.TextInput(attrs={"class": "form-control"}),
        }
        labels = {
            'reg': 'Region: '
        }

class AddCStatusForm(forms.ModelForm):
    class Meta:
        model = AddCStatus
        fields = [
            'status'
        ]
        widgets = {
            'status': forms.TextInput(attrs={"class": "form-control"}),
        }
        labels = {
            'status': 'Conservation Status: '
        }

class EditCStatusForm(forms.ModelForm):
    class Meta:
        model = EditCStatus
        fields = [
            'stat'
        ]
        widgets = {
            'stat': forms.TextInput(attrs={"class": "form-control"}),
        }
        labels = {
            'stat': 'Conservation Status: '
        }

class AddGroupForm(forms.ModelForm):
    class Meta:
        model = AddGroup
        fields = [
            'group'
        ]
        widgets = {
            'group': forms.TextInput(attrs={"class": "form-control"}),
        }
        labels = {
            'group': "Group: "
        }

class EditGroupForm(forms.ModelForm):
    class Meta:
        model = EditGroup
        fields = [
            'grp'
        ]
        widgets = {
            'grp': forms.TextInput(attrs={"class": "form-control"}),
        }
        labels = {
            'grp': "Group: "
        }
