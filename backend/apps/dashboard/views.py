from django.db.models import Count
from django.utils import timezone
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.audit.models import AuditLog
from apps.cases.models import Case
from apps.hearings.models import Hearing


class DashboardView(APIView):
    def get(self, request):
        counts = {s: 0 for s, _ in Case.STATUS_CHOICES}
        for row in Case.objects.filter(is_archived=False).values("status").annotate(n=Count("id")):
            counts[row["status"]] = row["n"]

        upcoming = (
            Hearing.objects.filter(status=Hearing.SCHEDULED, hearing_datetime__gte=timezone.now())
            .exclude(case__status="closed")
            .select_related("case")
            .order_by("hearing_datetime")[:10]
        )
        recent = AuditLog.objects.select_related("user")[:10]

        return Response({
            "case_counts": counts,
            "total_cases": sum(counts.values()),
            "upcoming_hearings": [
                {"id": h.id, "case_id": h.case_id, "case_number": h.case.case_number,
                 "hearing_datetime": h.hearing_datetime}
                for h in upcoming
            ],
            "recent_activity": [
                {"id": a.id, "action": a.action, "entity_type": a.entity_type, "entity_id": a.entity_id,
                 "user": a.user.username if a.user else None, "created_at": a.created_at}
                for a in recent
            ],
        })
