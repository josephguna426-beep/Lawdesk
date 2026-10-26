from rest_framework import serializers

from .models import Hearing, HearingParticipant


class HearingParticipantSerializer(serializers.ModelSerializer):
    class Meta:
        model = HearingParticipant
        fields = ["id", "party", "advocate", "name", "role"]


class HearingSerializer(serializers.ModelSerializer):
    participants = HearingParticipantSerializer(many=True, required=False)
    case_number = serializers.CharField(source="case.case_number", read_only=True)

    class Meta:
        model = Hearing
        fields = [
            "id", "case", "case_number", "hearing_datetime", "status", "proceedings",
            "judge_comments", "orders", "next_hearing_date", "rescheduled_from",
            "participants", "created_at", "updated_at",
        ]
        read_only_fields = ["rescheduled_from"]

    def validate_case(self, case):
        if case.status == "closed":
            raise serializers.ValidationError("Cannot add hearings to a closed case.")
        return case

    def create(self, validated_data):
        participants = validated_data.pop("participants", [])
        hearing = Hearing.objects.create(**validated_data)
        for p in participants:
            HearingParticipant.objects.create(hearing=hearing, **p)
        return hearing

    def update(self, instance, validated_data):
        validated_data.pop("participants", None)  # manage participants via dedicated endpoint later
        return super().update(instance, validated_data)


class RescheduleSerializer(serializers.Serializer):
    hearing_datetime = serializers.DateTimeField()
