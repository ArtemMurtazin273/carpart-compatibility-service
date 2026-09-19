from django.contrib.auth.models import AbstractUser
from django.db import models

from django.conf import settings


class Mechanic(AbstractUser):
    license_number = models.CharField(max_length=255, unique=True)

    class Meta:
        verbose_name = "mechanic"
        verbose_name_plural = "mechanics"
        ordering = ["username"]

    def __str__(self):
        return f"{self.username} ({self.first_name} {self.last_name})"


class Manufacturer(models.Model):
    name = models.CharField(max_length=255, unique=True)
    country = models.CharField(max_length=255)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return f"{self.name} ({self.country})"


class PartCategory(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name_plural = "part categories"
        ordering = ["name"]

    def __str__(self):
        return self.name


class Car(models.Model):
    make = models.CharField(max_length=255)
    model = models.CharField(max_length=255)
    year = models.IntegerField()

    class Meta:
        ordering = ["make", "model", "year"]
        constraints = [
            models.UniqueConstraint(
                fields=["make", "model", "year"],
                name="unique_car_specification"
            )
        ]

    def __str__(self):
        return f"{self.make} {self.model} ({self.year})"


class Part(models.Model):
    name = models.CharField(max_length=255)
    part_number = models.CharField(max_length=64, unique=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    manufacturer = models.ForeignKey(
        Manufacturer,
        on_delete=models.CASCADE,
        related_name="parts"
    )
    category = models.ForeignKey(
        PartCategory,
        on_delete=models.CASCADE,
        related_name="parts"
    )
    cars = models.ManyToManyField(
        Car,
        related_name="parts",
        blank=True
    )
    mechanics = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name="parts",
        blank=True
    )

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return f"{self.name} [{self.part_number}]"
