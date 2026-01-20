from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    complete_name = models.CharField()
    cpf = models.CharField(max_length=14, unique=True)
    phone = models.CharField(max_length=11, unique=True)
    birth_date = models.DateField()
