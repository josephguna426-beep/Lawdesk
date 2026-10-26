from django.db.models import Q
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from apps.audit.services import log_event

from .models import Case, CaseAdvocate, CaseClient, CaseParty
from .serializers import (
    CaseAdvocateSerializer, CaseClientSerializer, CasePartySerializer, CaseSerializer,
)


class CaseViewSet(viewsets.ModelViewSet):
    serializer_class = CaseSerializer

    def get_queryset(self):
        qs = Case.objects.select_related("court").prefetch_related(
            "caseclient_set", "caseparty_set", "caseadvocate_set"
        )
        p = self.request.query_params
        if p.get("q"):
            qs = qs.filter(Q(case_number__icontains=p["q"]) | Q(title__icontains=p["q"]))
        if p.get("status"):
            qs = qs.filter(status=p["status"])
        if p.get("court"):
            qs = qs.filter(court_id=p["court"])
        if p.get("date_from"):
            qs = qs.filter(filing_date__gte=p["date_from"])
        if p.get("date_to"):
            qs = qs.filter(filing_date__lte=p["date_to"])
        if p.get("archived") != "1":
            qs = qs.filter(is_archived=False)
        return qs

    def perform_create(self, serializer):
        case = serializer.save(created_by=self.request.user)
        log_event(self.request.user, "case.created", "case", case.id, request=self.request)

    def perform_update(self, serializer):
        case = serializer.save()
        log_event(self.request.user, "case.updated", "case", case.id,
                  changes=dict(self.request.data), request=self.request)

    @action(detail=True, methods=["post"])
    def archive(self, request, pk=None):
        case = self.get_object()
        case.is_archived = True
        case.save(update_fields=["is_archived", "updated_at"])
        log_event(request.user, "case.archived", "case", case.id, request=request)
        return Response(self.get_serializer(case).data)

    # --- links: POST {"client": id} / {"party": id, "role": ""} / {"advocate": id, "role": ""}
    @action(detail=True, methods=["post"], url_path="clients")
    def add_client(self, request, pk=None):
        ser = CaseClientSerializer(data=request.data)
        ser.is_valid(raise_exception=True)
        ser.save(case=self.get_object())
        return Response(ser.data, status=201)

    @action(detail=True, methods=["post"], url_path="parties")
    def add_party(self, request, pk=None):
        ser = CasePartySerializer(data=request.data)
        ser.is_valid(raise_exception=True)
        ser.save(case=self.get_object())
        return Response(ser.data, status=201)

    @action(detail=True, methods=["post"], url_path="advocates")
    def add_advocate(self, request, pk=None):
        ser = CaseAdvocateSerializer(data=request.data)
        ser.is_valid(raise_exception=True)
        ser.save(case=self.get_object())
        return Response(ser.data, status=201)
