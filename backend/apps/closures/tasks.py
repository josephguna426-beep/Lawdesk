import hashlib

from celery import shared_task
from django.utils import timezone

from apps.audit.services import log_event
from apps.common.storage import private_path

from .models import ClosurePDF
from .pdf import build_closure_pdf


@shared_task
def generate_closure_pdf(pdf_id):
    pdf = ClosurePDF.objects.select_related("case", "case__court", "closure", "generated_by").get(pk=pdf_id)
    pdf.status = ClosurePDF.PROCESSING
    pdf.save(update_fields=["status"])
    try:
        key = f"closure_pdfs/{pdf.case_id}/v{pdf.version}.pdf"
        path = private_path(key)
        hearings = list(pdf.case.hearings.order_by("hearing_datetime"))
        build_closure_pdf(pdf.case, pdf.closure, hearings, path)
        pdf.sha256 = hashlib.sha256(path.read_bytes()).hexdigest()
        pdf.storage_key = key
        pdf.status = ClosurePDF.READY
        pdf.generated_at = timezone.now()
        pdf.error_message = ""
        pdf.save()
        log_event(pdf.generated_by, "closure_pdf.generated", "closure_pdf", pdf.id)
    except Exception as exc:  # closure stays saved; failure recorded, retry available
        pdf.status = ClosurePDF.FAILED
        pdf.error_message = str(exc)[:1000]
        pdf.save(update_fields=["status", "error_message"])
        log_event(pdf.generated_by, "closure_pdf.failed", "closure_pdf", pdf.id, changes={"error": pdf.error_message})
