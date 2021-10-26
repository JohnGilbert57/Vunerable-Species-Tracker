"""Created forms that will be called to pass forms to the html"""
# Johnny Gilbert
# Ohio University
# the format for the user login; creates the objects basesd upon the models and sets the data
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User



class NewUserForm(UserCreationForm):
    """login form"""
    class Meta:
        model = User
        fields = ["username"]
        widgets = {
            'username': forms.TextInput(attrs={"class": "form-control"}),
        }
        labels = {
            'username': 'Username',
        }
        