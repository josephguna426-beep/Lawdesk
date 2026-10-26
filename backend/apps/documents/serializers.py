import os

from django.conf import settings
from rest_framework import serializers

from .models import Document


class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = ["id", "case", "title", "original_name", "content_type", "size_bytes", "uploaded_by", "uploaded_at"]
        read_only_fields = fields


class DocumentUploadSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=255)
    file = serializers.FileField()

    def validate_file(self, f):
        ext = os.path.splitext(f.name)[1].lower()
        if ext not in settings.ALLOWED_UPLOAD_EXTENSIONS:
            raise serializers.ValidationError("File type not allowed.")
        if f.size > settings.MAX_UPLOAD_MB * 1024 * 1024:
            raise serializers.ValidationError(f"File exceeds {settings.MAX_UPLOAD_MB} MB.")
        if f.content_type not in settings.ALLOWED_UPLOAD_MIME_TYPES:
            raise serializers.ValidationError("Unsupported content type.")
        return f
