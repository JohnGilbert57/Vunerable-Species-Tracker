"""Created forms that will be called to pass forms to the html"""
# Johnny Gilbert
# Ohio University
# the format for the user login; creates the objects basesd upon the models and sets the data
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Species
from myapp.database import *

class EditSpeciesForm(forms.ModelForm):
    
    """creating a new hobby"""
    class Meta:
        def getRegion():
            query = db_query('SELECT * FROM REGION')
            regions = {}
            for r in query:
                regions.update(query)
            return regions
        model = Species
        fields = [
            'commonName',
            'scientificName',
            'region',
            'conservationStatus',
            'group'
        ]
        regions = getRegion()
        REGION = (
            for r in region:
                (r, r),
        )
        STATUS = (
        ('Endangered','Endangered'),
        ('Threatened','Threatened'),
        ('Experimental','Experimental Population, Non-Essential'), 
        ('Similarity','Southeast'),
        ('Northeast', 'Northeast'),
        ('Mountain-Prarie', 'Mountain-Praries'),
        ('Alaska', 'Alaska'),
        )
        widgets = {
            'commonName': forms.TextInput(attrs={"class": "form-control"}),
            'scientificName': forms.TextInput(attrs={"class": "form-control"}),
            'conservationStatus': forms.Select(attrs={"class": "form-control"}),
            'region': forms.Select(attrs={"class": "form-control"}, choices = REGION),
            'conservationStatus': forms.Select(attrs={"class": "form-control"}),
            'group': forms.Select(attrs={"class": "form-control"})
        }
        labels = {
            'commonName': 'Common Name: ',
            'scientificName': 'Scientific Name: ',
            'region': 'Region: ',
            'conservationStatus': 'Conservation Status: ',
            'group': 'Group: '
        }

        
