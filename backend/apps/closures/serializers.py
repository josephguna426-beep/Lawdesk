from rest_framework import serializers

from .models import CaseClosure, ClosurePDF


class CloseCaseSerializer(serializers.Serializer):
    outcome = serializers.CharField(max_length=255)
    closure_date = serializers.DateField()
    remarks = serializers.CharField(required=False, allow_blank=True)
    final_order_reference = serializers.CharField(required=False, allow_blank=True, max_length=255)


class CaseClosureSerializer(serializers.ModelSerializer):
    class Meta:
        model = CaseClosure
        fields = ["id", "case", "outcome", "closure_date", "remarks", "final_order_reference", "closed_by", "created_at"]


class ClosurePDFSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClosurePDF
        fields = ["id", "case", "version", "status", "sha256", "error_message", "generated_by", "generated_at", "created_at"]
