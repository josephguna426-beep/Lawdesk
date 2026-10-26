import hashlib

from django.db import transaction
from django.http import FileResponse, Http404
from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.audit.services import log_event
from apps.cases.models import Case
from apps.common.storage import private_path

from .models import CaseClosure, ClosurePDF
from .serializers import CaseClosureSerializer, CloseCaseSerializer, ClosurePDFSerializer
from .tasks import generate_closure_pdf


def _next_version(case):
    last = ClosurePDF.objects.filter(case=case).order_by("-version").first()
    return (last.version + 1) if last else 1


class CloseCaseView(APIView):
    def post(self, request, case_id):
        ser = CloseCaseSerializer(data=request.data)
        ser.is_valid(raise_exception=True)
        with transaction.atomic():
            case = get_object_or_404(Case.objects.select_for_update(), pk=case_id)
            if case.status == Case.CLOSED or CaseClosure.objects.filter(case=case).exists():
                return Response({"detail": "Case is already closed."}, status=status.HTTP_400_BAD_REQUEST)
            closure = CaseClosure.objects.create(case=case, closed_by=request.user, **ser.validated_data)
            case.status = Case.CLOSED
            case.save(update_fields=["status", "updated_at"])
            pdf = ClosurePDF.objects.create(
                case=case, closure=closure, version=_next_version(case), generated_by=request.user
            )
            log_event(request.user, "case.closed", "case", case.id,
                      changes=ser.validated_data, request=request)
            # queue only after the DB commit succeeds
            transaction.on_commit(lambda: generate_closure_pdf.delay(pdf.id))
        return Response(CaseClosureSerializer(closure).data, status=status.HTTP_201_CREATED)


class CaseClosurePDFsView(APIView):
    def get(self, request, case_id):
        pdfs = ClosurePDF.objects.filter(case_id=case_id)
        return Response(ClosurePDFSerializer(pdfs, many=True).data)

    # Regenerate: always creates a NEW version, never overwrites an earlier one.
    def post(self, request, case_id):
        case = get_object_or_404(Case, pk=case_id)
        closure = get_object_or_404(CaseClosure, case=case)
        with transaction.atomic():
            pdf = ClosurePDF.objects.create(
                case=case, closure=closure, version=_next_version(case), generated_by=request.user
            )
            transaction.on_commit(lambda: generate_closure_pdf.delay(pdf.id))
        return Response(ClosurePDFSerializer(pdf).data, status=status.HTTP_201_CREATED)


class RetryClosurePDFView(APIView):
    def post(self, request, pk):
        pdf = get_object_or_404(ClosurePDF, pk=pk)
        if pdf.status != ClosurePDF.FAILED:
            return Response({"detail": "Only failed PDFs can be retried."}, status=400)
        pdf.status = ClosurePDF.PENDING
        pdf.error_message = ""
        pdf.save(update_fields=["status", "error_message"])
        generate_closure_pdf.delay(pdf.id)
        return Response(ClosurePDFSerializer(pdf).data)


class DownloadClosurePDFView(APIView):
    def get(self, request, pk):
        pdf = get_object_or_404(ClosurePDF, pk=pk, status=ClosurePDF.READY)
        path = private_path(pdf.storage_key)
        if not path.exists():
            raise Http404("File missing")
        # integrity check before serving
        if hashlib.sha256(path.read_bytes()).hexdigest() != pdf.sha256:
            return Response({"detail": "Integrity check failed."}, status=500)
        log_event(request.user, "closure_pdf.downloaded", "closure_pdf", pdf.id, request=request)
        return FileResponse(open(path, "rb"), as_attachment=True,
                            filename=f"case-{pdf.case_id}-closure-v{pdf.version}.pdf")
