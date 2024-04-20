from django.db import models

# Create your models here.

#for test 
class User(models.Model):
    id=models.AutoField(primary_key=True)