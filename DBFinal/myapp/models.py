"""There are two models for each page so we can specify which div to grab when doing the javascript"""
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator


class AddSpecies(models.Model):
    commonName = models.CharField(max_length=30)
    scientificName = models.CharField(max_length=30)
    region = models.CharField(max_length=30)
    conservationStatus = models.CharField(max_length=30)
    group = models.CharField(max_length=30)

class EditSpecies(models.Model):
    cName = models.CharField(max_length=30)
    sName = models.CharField(max_length=30)
    reg = models.CharField(max_length=30)
    cStatus = models.CharField(max_length=30)
    grp = models.CharField(max_length=30)

class AddRegion(models.Model):
    region = models.CharField(max_length=30)

class EditRegion(models.Model):
    reg = models.CharField(max_length = 30)

class AddCStatus(models.Model):
    status = models.CharField(max_length = 30)

class EditCStatus(models.Model):
    stat = models.CharField(max_length = 30)

class AddGroup(models.Model):
    group = models.CharField(max_length = 30)

class EditGroup(models.Model):
    grp = models.CharField(max_length = 30)