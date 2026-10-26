from django.db import models

from apps.common.models import TimeStampedModel


class Client(TimeStampedModel):
    full_name = models.CharField(max_length=255)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=30, blank=True)
    address = models.TextField(blank=True)

    class Meta:
        ordering = ["full_name"]

    def __str__(self):
        return self.full_name


class Party(TimeStampedModel):
    full_name = models.CharField(max_length=255)
    party_type = models.CharField(max_length=100, blank=True)  # e.g. petitioner, respondent, witness
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=30, blank=True)
    address = models.TextField(blank=True)

    class Meta:
        ordering = ["full_name"]
        verbose_name_plural = "parties"

    def __str__(self):
        return self.full_name
