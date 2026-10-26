from django.conf import settings
from django.db import models

from apps.common.models import TimeStampedModel


class Case(TimeStampedModel):
    OPEN = "open"
    IN_PROGRESS = "in_progress"
    ON_HOLD = "on_hold"
    CLOSED = "closed"
    STATUS_CHOICES = [
        (OPEN, "Open"),
        (IN_PROGRESS, "In progress"),
        (ON_HOLD, "On hold"),
        (CLOSED, "Closed"),
    ]
    # allowed manual transitions (closing is only done via the close endpoint)
    ALLOWED_TRANSITIONS = {
        OPEN: {IN_PROGRESS, ON_HOLD},
        IN_PROGRESS: {OPEN, ON_HOLD},
        ON_HOLD: {OPEN, IN_PROGRESS},
        CLOSED: set(),
    }

    case_number = models.CharField(max_length=100)
    title = models.CharField(max_length=255)
    case_type = models.CharField(max_length=100, blank=True)
    description = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=OPEN)
    court = models.ForeignKey("courts.Court", on_delete=models.PROTECT, related_name="cases")
    filing_date = models.DateField()
    is_archived = models.BooleanField(default=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="cases_created")

    clients = models.ManyToManyField("parties.Client", through="CaseClient", related_name="cases")
    parties = models.ManyToManyField("parties.Party", through="CaseParty", related_name="cases")
    advocates = models.ManyToManyField("courts.Advocate", through="CaseAdvocate", related_name="cases")

    class Meta:
        ordering = ["-filing_date", "-id"]
        constraints = [
            models.UniqueConstraint(fields=["court", "case_number"], name="uniq_case_number_per_court"),
        ]

    def __str__(self):
        return f"{self.case_number} - {self.title}"


class CaseClient(models.Model):
    case = models.ForeignKey(Case, on_delete=models.CASCADE)
    client = models.ForeignKey("parties.Client", on_delete=models.PROTECT)

    class Meta:
        constraints = [models.UniqueConstraint(fields=["case", "client"], name="uniq_case_client")]


class CaseParty(models.Model):
    case = models.ForeignKey(Case, on_delete=models.CASCADE)
    party = models.ForeignKey("parties.Party", on_delete=models.PROTECT)
    role = models.CharField(max_length=100, blank=True)

    class Meta:
        constraints = [models.UniqueConstraint(fields=["case", "party", "role"], name="uniq_case_party_role")]


class CaseAdvocate(models.Model):
    case = models.ForeignKey(Case, on_delete=models.CASCADE)
    advocate = models.ForeignKey("courts.Advocate", on_delete=models.PROTECT)
    role = models.CharField(max_length=100, blank=True)

    class Meta:
        constraints = [models.UniqueConstraint(fields=["case", "advocate", "role"], name="uniq_case_advocate_role")]
