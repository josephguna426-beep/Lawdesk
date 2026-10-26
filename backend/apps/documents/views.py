import os
import uuid

from django.http import FileResponse, Http404
from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.audit.services import log_event
from apps.cases.models import Case
from apps.common.storage import private_path

from .models import Document
from .serializers import DocumentSerializer, DocumentUploadSerializer


class CaseDocumentsView(APIView):
    parser_classes = [MultiPartParser]

    def get(self, request, case_id):
        case = get_object_or_404(Case, pk=case_id)
        docs = Document.objects.filter(case=case)
        return Response(DocumentSerializer(docs, many=True).data)

    def post(self, request, case_id):
        case = get_object_or_404(Case, pk=case_id)
        ser = DocumentUploadSerializer(data=request.data)
        ser.is_valid(raise_exception=True)
        upload = ser.validated_data["file"]
        safe_name = os.path.basename(upload.name)
        key = f"documents/{case.id}/{uuid.uuid4().hex}_{safe_name}"
        with open(private_path(key), "wb") as out:
            for chunk in upload.chunks():
                out.write(chunk)
        doc = Document.objects.create(
            case=case, title=ser.validated_data["title"], original_name=safe_name,
            content_type=upload.content_type, size_bytes=upload.size,
            storage_key=key, uploaded_by=request.user,
        )
        log_event(request.user, "document.uploaded", "document", doc.id, request=request)
        return Response(DocumentSerializer(doc).data, status=status.HTTP_201_CREATED)


class DocumentDownloadView(APIView):
    def get(self, request, pk):
        doc = get_object_or_404(Document, pk=pk)
        path = private_path(doc.storage_key)
        if not path.exists():
            raise Http404("File missing")
        log_event(request.user, "document.downloaded", "document", doc.id, request=request)
        return FileResponse(open(path, "rb"), as_attachment=True, filename=doc.original_name)
