from django.db import models
from django.contrib.auth.models import AbstractUser

from .utils import validate_cpf

class User(AbstractUser):
    complete_name = models.CharField()
    cpf = models.CharField(
        max_length=14, unique=True,
        validators=[validate_cpf],
    )
    phone = models.CharField(max_length=11, unique=True)
    birth_date = models.DateField()
