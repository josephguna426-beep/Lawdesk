from django.conf import settings
from django.db import models


class Reminder(models.Model):
    DAY_BEFORE = "day_before"
    HEARING_DAY = "hearing_day"
    TYPE_CHOICES = [(DAY_BEFORE, "Day before (09:00)"), (HEARING_DAY, "Hearing day (08:00)")]
    PENDING = "pending"
    SENT = "sent"
    FAILED = "failed"
    SUPPRESSED = "suppressed"
    STATUS_CHOICES = [(PENDING, "Pending"), (SENT, "Sent"), (FAILED, "Failed"), (SUPPRESSED, "Suppressed")]

    hearing = models.ForeignKey("hearings.Hearing", on_delete=models.CASCADE, related_name="reminders")
    reminder_type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    scheduled_for = models.DateTimeField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=PENDING)
    idempotency_key = models.CharField(max_length=200, unique=True)
    attempts = models.PositiveIntegerField(default=0)
    last_error = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)


class Notification(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="notifications")
    reminder = models.OneToOneField(Reminder, null=True, blank=True, on_delete=models.SET_NULL)
    hearing = models.ForeignKey("hearings.Hearing", null=True, blank=True, on_delete=models.SET_NULL)
    title = models.CharField(max_length=255)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
