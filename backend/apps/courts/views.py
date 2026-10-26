from django.db.models import Q
from rest_framework import viewsets

from .models import Advocate, Court
from .serializers import AdvocateSerializer, CourtSerializer


class CourtViewSet(viewsets.ModelViewSet):
    serializer_class = CourtSerializer

    def get_queryset(self):
        qs = Court.objects.all()
        q = self.request.query_params.get("q")
        if q:
            qs = qs.filter(Q(name__icontains=q) | Q(location__icontains=q))
        return qs


class AdvocateViewSet(viewsets.ModelViewSet):
    serializer_class = AdvocateSerializer

    def get_queryset(self):
        qs = Advocate.objects.all()
        q = self.request.query_params.get("q")
        if q:
            qs = qs.filter(Q(full_name__icontains=q) | Q(registration_number__icontains=q))
        return qs
