from django.db.models import Count, Q
from django.utils import timezone
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.cases.models import Case
from apps.courts.models import Advocate, Court
from apps.hearings.models import Hearing
from apps.parties.models import Client, Party


class GlobalSearchView(APIView):
    def get(self, request):
        q = (request.query_params.get("q") or "").strip()
        if len(q) < 2:
            return Response({"cases": [], "clients": [], "parties": [], "courts": [], "advocates": []})
        return Response({
            "cases": list(Case.objects.filter(Q(case_number__icontains=q) | Q(title__icontains=q))
                          .values("id", "case_number", "title", "status")[:10]),
            "clients": list(Client.objects.filter(full_name__icontains=q).values("id", "full_name")[:10]),
            "parties": list(Party.objects.filter(full_name__icontains=q).values("id", "full_name")[:10]),
            "courts": list(Court.objects.filter(name__icontains=q).values("id", "name")[:10]),
            "advocates": list(Advocate.objects.filter(full_name__icontains=q).values("id", "full_name")[:10]),
        })


class CaseStatusReportView(APIView):
    def get(self, request):
        qs = Case.objects.all()
        p = request.query_params
        if p.get("date_from"):
            qs = qs.filter(filing_date__gte=p["date_from"])
        if p.get("date_to"):
            qs = qs.filter(filing_date__lte=p["date_to"])
        if p.get("court"):
            qs = qs.filter(court_id=p["court"])
        rows = qs.values("status").annotate(count=Count("id")).order_by("status")
        return Response({"results": list(rows)})


class UpcomingHearingsReportView(APIView):
    def get(self, request):
        qs = (Hearing.objects.filter(status=Hearing.SCHEDULED, hearing_datetime__gte=timezone.now())
              .exclude(case__status="closed").select_related("case", "case__court"))
        p = request.query_params
        if p.get("date_to"):
            qs = qs.filter(hearing_datetime__date__lte=p["date_to"])
        if p.get("court"):
            qs = qs.filter(case__court_id=p["court"])
        return Response({"results": [
            {"id": h.id, "case_number": h.case.case_number, "court": h.case.court.name,
             "hearing_datetime": h.hearing_datetime}
            for h in qs.order_by("hearing_datetime")[:200]
        ]})
