from django.db import models

from apps.common.models import TimeStampedModel


class Court(TimeStampedModel):
    name = models.CharField(max_length=255)
    court_type = models.CharField(max_length=100, blank=True)
    location = models.CharField(max_length=255, blank=True)

    class Meta:
        ordering = ["name"]
        constraints = [models.UniqueConstraint(fields=["name", "location"], name="uniq_court_name_location")]

    def __str__(self):
        return self.name


class Advocate(TimeStampedModel):
    full_name = models.CharField(max_length=255)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=30, blank=True)
    registration_number = models.CharField(max_length=100, unique=True)
    address = models.TextField(blank=True)

    class Meta:
        ordering = ["full_name"]

    def __str__(self):
        return self.full_name
