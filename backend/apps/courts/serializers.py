from rest_framework import serializers

from .models import Advocate, Court


class CourtSerializer(serializers.ModelSerializer):
    class Meta:
        model = Court
        fields = "__all__"


class AdvocateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Advocate
        fields = "__all__"
