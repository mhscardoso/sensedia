from django.db import models

from projects.models import Project
from users.models import User


class Status(models.TextChoices):
    PENDING = "PENDING", "Pending"
    WORKING = "WORKING", "Working"
    DONE = "DONE", "Done"


class Items(models.Model):
    title = models.CharField(max_length=20)
    description = models.CharField(max_length=100)
    status = models.CharField(
        max_length=10,
        choices=Status.choices,
        default=Status.PENDING,
    )

    forecast = models.DateField(null=True)

    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='items')
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='items')
