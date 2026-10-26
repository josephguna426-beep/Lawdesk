from rest_framework import mixins, viewsets

from .models import AuditLog
from .serializers import AuditLogSerializer


class AuditLogViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    # read-only: audit records are never edited or deleted through the API
    serializer_class = AuditLogSerializer

    def get_queryset(self):
        qs = AuditLog.objects.select_related("user")
        p = self.request.query_params
        if p.get("entity_type"):
            qs = qs.filter(entity_type=p["entity_type"])
        if p.get("entity_id"):
            qs = qs.filter(entity_id=p["entity_id"])
        if p.get("action"):
            qs = qs.filter(action=p["action"])
        return qs
