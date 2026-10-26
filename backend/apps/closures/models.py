from django.conf import settings
from django.db import models


class CaseClosure(models.Model):
    case = models.OneToOneField("cases.Case", on_delete=models.PROTECT, related_name="closure")
    outcome = models.CharField(max_length=255)
    closure_date = models.DateField()
    remarks = models.TextField(blank=True)
    final_order_reference = models.CharField(max_length=255, blank=True)
    closed_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True)


class ClosurePDF(models.Model):
    PENDING = "pending"
    PROCESSING = "processing"
    READY = "ready"
    FAILED = "failed"
    STATUS_CHOICES = [(PENDING, "Pending"), (PROCESSING, "Processing"), (READY, "Ready"), (FAILED, "Failed")]

    case = models.ForeignKey("cases.Case", on_delete=models.PROTECT, related_name="closure_pdfs")
    closure = models.ForeignKey(CaseClosure, on_delete=models.PROTECT, related_name="pdfs")
    version = models.PositiveIntegerField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=PENDING)
    storage_key = models.CharField(max_length=500, blank=True)
    sha256 = models.CharField(max_length=64, blank=True)
    error_message = models.TextField(blank=True)
    generated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    generated_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-version"]
        constraints = [models.UniqueConstraint(fields=["case", "version"], name="uniq_pdf_version_per_case")]
