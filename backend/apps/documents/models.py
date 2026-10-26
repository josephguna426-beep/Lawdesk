from django.conf import settings
from django.db import models


class Document(models.Model):
    case = models.ForeignKey("cases.Case", on_delete=models.PROTECT, related_name="documents")
    title = models.CharField(max_length=255)
    original_name = models.CharField(max_length=255)
    content_type = models.CharField(max_length=100)
    size_bytes = models.PositiveBigIntegerField()
    storage_key = models.CharField(max_length=500, unique=True)  # relative to PRIVATE_STORAGE_ROOT
    uploaded_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-uploaded_at"]
