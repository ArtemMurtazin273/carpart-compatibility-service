from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models


class Mechanic(AbstractUser):
    license_number = models.CharField(max_length=255, unique=True)

    class Meta:
        verbose_name = "mechanic"
        verbose_name_plural = "mechanics"
        ordering = ["username"]

    def __str__(self):
        return f"{self.username} ({self.first_name} {self.last_name})"
