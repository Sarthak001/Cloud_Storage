from django.db import models
import os, time

# Create your models here.
class UserDetails(models.Model):
    firstName = models.CharField(max_length=50)
    lastName = models.CharField(max_length=50)
    password = models.CharField(max_length=100)
    address = models.CharField(max_length=250)
    city = models.CharField(max_length=50)
    country = models.CharField(max_length=50)
    email = models.EmailField(default='', unique=True)

class FileDetails(models.Model):
    fileName = models.CharField(max_length=100)
    user = models.EmailField()
    lastModified = models.CharField(max_length=100)
    size = models.CharField(max_length=20)
