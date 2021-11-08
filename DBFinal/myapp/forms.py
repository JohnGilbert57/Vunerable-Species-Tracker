"""Created forms that will be called to pass forms to the html"""
# Johnny Gilbert
# Ohio University
# the format for the user login; creates the objects basesd upon the models and sets the data
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Species
from myapp.database import *

class EditOrAddSpeciesForm(forms.ModelForm):
    
    """creating a new hobby"""
    class Meta:
        model = Species
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
