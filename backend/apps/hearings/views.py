from django.db import transaction
from rest_framework import mixins, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone

from apps.audit.services import log_event
from apps.notifications.services import suppress_pending_reminders

from .models import Hearing
from .serializers import HearingSerializer, RescheduleSerializer


class HearingViewSet(
    mixins.CreateModelMixin, mixins.RetrieveModelMixin, mixins.UpdateModelMixin,
    mixins.ListModelMixin, viewsets.GenericViewSet,
):
    # No DELETE: every hearing is kept as a historical record.
    serializer_class = HearingSerializer

    def get_queryset(self):
        qs = Hearing.objects.select_related("case").prefetch_related("participants")
        p = self.request.query_params
        if p.get("case"):
            qs = qs.filter(case_id=p["case"])
        if p.get("status"):
            qs = qs.filter(status=p["status"])
        if p.get("upcoming") == "1":
            qs = qs.filter(status=Hearing.SCHEDULED, hearing_datetime__gte=timezone.now())
        return qs

    @action(detail=True, methods=["post"])
    def reschedule(self, request, pk=None):
        old = self.get_object()
        ser = RescheduleSerializer(data=request.data)
        ser.is_valid(raise_exception=True)
        with transaction.atomic():
            old.status = Hearing.RESCHEDULED
            old.save(update_fields=["status", "updated_at"])
            new = Hearing.objects.create(
                case=old.case,
                hearing_datetime=ser.validated_data["hearing_datetime"],
                rescheduled_from=old,
            )
            suppress_pending_reminders(old)
            log_event(request.user, "hearing.rescheduled", "hearing", old.id,
                      changes={"new_hearing": new.id}, request=request)
        return Response(self.get_serializer(new).data, status=201)

    @action(detail=True, methods=["post"])
    def cancel(self, request, pk=None):
        hearing = self.get_object()
        with transaction.atomic():
            hearing.status = Hearing.CANCELLED
            hearing.save(update_fields=["status", "updated_at"])
            suppress_pending_reminders(hearing)
            log_event(request.user, "hearing.cancelled", "hearing", hearing.id, request=request)
        return Response(self.get_serializer(hearing).data)
