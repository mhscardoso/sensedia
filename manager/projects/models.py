from django.db import models
from users.models import User

class Project(models.Model):
    name = models.CharField(max_length=20)
    description = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField()

    owner = models.ForeignKey(User, on_delete=models.CASCADE)
