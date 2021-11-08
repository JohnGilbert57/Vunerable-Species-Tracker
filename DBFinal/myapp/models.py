from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

class Species(models.Model):
    commonName = models.CharField(max_length=30)
    scientificName = models.CharField(max_length=30)
    region = models.CharField(max_length=30)
    conservationStatus = models.CharField(max_length=30)
    group = models.CharField(max_length=30)

