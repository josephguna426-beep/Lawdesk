from django.db import models

from apps.common.models import TimeStampedModel


class Hearing(TimeStampedModel):
    SCHEDULED = "scheduled"
    COMPLETED = "completed"
    RESCHEDULED = "rescheduled"
    CANCELLED = "cancelled"
    STATUS_CHOICES = [
        (SCHEDULED, "Scheduled"),
        (COMPLETED, "Completed"),
        (RESCHEDULED, "Rescheduled"),
        (CANCELLED, "Cancelled"),
    ]

    case = models.ForeignKey("cases.Case", on_delete=models.PROTECT, related_name="hearings")
    hearing_datetime = models.DateTimeField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=SCHEDULED)
    proceedings = models.TextField(blank=True)
    judge_comments = models.TextField(blank=True)
    orders = models.TextField(blank=True)
    next_hearing_date = models.DateField(null=True, blank=True)
    rescheduled_from = models.ForeignKey(
        "self", null=True, blank=True, on_delete=models.SET_NULL, related_name="rescheduled_to"
    )

    class Meta:
        ordering = ["hearing_datetime"]

    def __str__(self):
        return f"{self.case_id} @ {self.hearing_datetime:%Y-%m-%d %H:%M}"


class HearingParticipant(models.Model):
    hearing = models.ForeignKey(Hearing, on_delete=models.CASCADE, related_name="participants")
    party = models.ForeignKey("parties.Party", null=True, blank=True, on_delete=models.SET_NULL)
    advocate = models.ForeignKey("courts.Advocate", null=True, blank=True, on_delete=models.SET_NULL)
    name = models.CharField(max_length=255, blank=True)
    role = models.CharField(max_length=100, blank=True)
