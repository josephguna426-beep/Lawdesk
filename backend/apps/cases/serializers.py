from rest_framework import serializers

from .models import Case, CaseAdvocate, CaseClient, CaseParty


class CaseClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = CaseClient
        fields = ["id", "client"]


class CasePartySerializer(serializers.ModelSerializer):
    class Meta:
        model = CaseParty
        fields = ["id", "party", "role"]


class CaseAdvocateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CaseAdvocate
        fields = ["id", "advocate", "role"]


class CaseSerializer(serializers.ModelSerializer):
    court_name = serializers.CharField(source="court.name", read_only=True)
    created_by = serializers.PrimaryKeyRelatedField(read_only=True)
    case_clients = CaseClientSerializer(source="caseclient_set", many=True, read_only=True)
    case_parties = CasePartySerializer(source="caseparty_set", many=True, read_only=True)
    case_advocates = CaseAdvocateSerializer(source="caseadvocate_set", many=True, read_only=True)

    class Meta:
        model = Case
        fields = [
            "id", "case_number", "title", "case_type", "description", "status", "court", "court_name",
            "filing_date", "is_archived", "created_by", "created_at", "updated_at",
            "case_clients", "case_parties", "case_advocates",
        ]
        read_only_fields = ["is_archived"]

    def validate_status(self, value):
        if self.instance is None:
            if value == Case.CLOSED:
                raise serializers.ValidationError("Use the close-case endpoint to close a case.")
            return value
        if value == self.instance.status:
            return value
        if value == Case.CLOSED:
            raise serializers.ValidationError("Use the close-case endpoint to close a case.")
        if value not in Case.ALLOWED_TRANSITIONS.get(self.instance.status, set()):
            raise serializers.ValidationError(f"Cannot change status from {self.instance.status} to {value}.")
        return value
