from django.urls import path

from . import views

urlpatterns = [
    path("cases/<int:case_id>/documents/", views.CaseDocumentsView.as_view(), name="case-documents"),
    path("documents/<int:pk>/download/", views.DocumentDownloadView.as_view(), name="document-download"),
]
