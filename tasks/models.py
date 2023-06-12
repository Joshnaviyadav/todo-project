from django.db import models
from django.conf import settings

class ToDo(models.Model):
    userName = models.CharField(max_length=20)
    task  = models.CharField(max_length=200)
    discription = models.CharField(max_length=1000,blank=True,null=True)
    createdDate = models.DateField()

