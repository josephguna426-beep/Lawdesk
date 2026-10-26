from django.db.models import Q
from rest_framework import viewsets

from .models import Client, Party
from .serializers import ClientSerializer, PartySerializer


def _search(qs, request):
    q = request.query_params.get("q")
    if q:
        qs = qs.filter(Q(full_name__icontains=q) | Q(phone__icontains=q) | Q(email__icontains=q))
    return qs


class ClientViewSet(viewsets.ModelViewSet):
    serializer_class = ClientSerializer

    def get_queryset(self):
        return _search(Client.objects.all(), self.request)


class PartyViewSet(viewsets.ModelViewSet):
    serializer_class = PartySerializer

    def get_queryset(self):
        return _search(Party.objects.all(), self.request)
