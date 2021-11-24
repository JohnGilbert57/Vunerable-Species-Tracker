"""Created forms that will be called to pass forms to the html"""
# Johnny Gilbert
# Nathaniel Buchanan
# Ohio University
# the format for the user login; creates the objects basesd upon the models and sets the data
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import *
from myapp.database import *

class AddSpeciesForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(self.__class__, self).__init__(*args, **kwargs)
        REGION = to_tuples(db_query('select region_id,region_name from region where deleted = 0 order by region_name'))
        STATUS = to_tuples(db_query('select status_id,status_name from status where deleted = 0 order by status_name'))
        GROUP = to_tuples(db_query('select group_id,group_name from species_group where deleted = 0 order by group_name'))
        self.fields['region'].choices = REGION
        self.fields['conservationStatus'].choices = STATUS
        self.fields['group'].choices = GROUP
    commonName = forms.CharField(label='Common Name', max_length=100)
    scientificName = forms.CharField(label='Scientific Name', max_length=100)
    region = forms.ChoiceField(label='Region')
    conservationStatus = forms.ChoiceField(label='Conservation Status')
    group = forms.ChoiceField(label='Group')

class EditSpeciesForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(self.__class__, self).__init__(*args, **kwargs)
        REGION = to_tuples(db_query('select region_id,region_name from region where deleted = 0 order by region_name'))
        STATUS = to_tuples(db_query('select status_id,status_name from status where deleted = 0 order by status_name'))
        GROUP = to_tuples(db_query('select group_id,group_name from species_group where deleted = 0 order by group_name'))
        self.fields['reg'].choices = REGION
        self.fields['cStatus'].choices = STATUS
        self.fields['grp'].choices = GROUP
    cName = forms.CharField(label='Common Name: ', max_length=100)
    sName = forms.CharField(label='Scientific Name: ', max_length=100)
    reg = forms.ChoiceField(label='Region: ')
    cStatus = forms.ChoiceField(label='Conservation Status: ')
    grp = forms.ChoiceField(label='Group: ')

class AddRegionForm(forms.Form):
    region = forms.CharField(label='Region: ', max_length=100)

class EditRegionForm(forms.Form):
    reg = forms.CharField(label='Region: ', max_length=100)

class AddCStatusForm(forms.Form):
    status = forms.CharField(label='Conservation Status: ', max_length=100)

class EditCStatusForm(forms.Form):
    stat = forms.CharField(label='Conservation Status: ', max_length=100)

class AddGroupForm(forms.Form):
    group = forms.CharField(label='Group: ', max_length=100)

class EditGroupForm(forms.Form):
    grp = forms.CharField(label='Group: ', max_length=100)

class FilterSpeciesForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(self.__class__, self).__init__(*args, **kwargs)
        REGION = to_tuples(db_query('select 0, "---" UNION select region_id, region_name from region where deleted = 0 order by region_name'))
        STATUS = to_tuples(db_query('select 0, "---" UNION select status_id, status_name from status where deleted = 0 order by status_name '))
        GROUP = to_tuples(db_query('select 0, "---" UNION select group_id, group_name from species_group  where deleted = 0 order by group_name'))
        self.fields['fReg'].choices = REGION
        self.fields['fCStatus'].choices = STATUS
        self.fields['fGrp'].choices = GROUP
    fCName = forms.CharField(label='Common Name: ',required=False, max_length=100)
    fSName = forms.CharField(label='Scientific Name: ',required=False, max_length=100)
    fReg = forms.ChoiceField(label='Region: ', required = False)
    fCStatus = forms.ChoiceField(label='Conservation Status: ', required = False)
    fGrp = forms.ChoiceField(label='Group: ', required = False)

class FilterRegionForm(forms.Form):
    fRegion = forms.CharField(label = 'Region: ', required = False, max_length = 100)

class FilterStatusForm(forms.Form):
    fStatus = forms.CharField(label = 'Conservation Status: ', required = False, max_length = 100)

class FilterGroupForm(forms.Form):
    fGroup = forms.CharField(label = 'Group: ', required = False, max_length = 100)

class FilterEducationListForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(self.__class__, self).__init__(*args, **kwargs)
        REGION = to_tuples(db_query('select 0, "---" UNION select region_id, region_name from region where deleted = 0 order by region_name'))
        STATUS = to_tuples(db_query('select 0, "---" UNION select status_id, status_name from status where deleted = 0 order by status_name '))
        self.fields['fRegion'].choices = REGION
        self.fields['fConservationStatus'].choices = STATUS
    fCommonName = forms.CharField(label = 'Common Name: ', required = False, max_length = 100)
    fScientificName = forms.CharField(label = "Scientific Name: ", required = False, max_length = 100)
    fRegion = forms.ChoiceField(label = "Region: ", required = False)
    fConservationStatus = forms.ChoiceField(label = "Conservation Status: ", required = False)
