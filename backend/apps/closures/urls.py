from django.urls import path

from . import views

urlpatterns = [
    path("cases/<int:case_id>/close/", views.CloseCaseView.as_view(), name="case-close"),
    path("cases/<int:case_id>/closure-pdfs/", views.CaseClosurePDFsView.as_view(), name="case-closure-pdfs"),
    path("closure-pdfs/<int:pk>/retry/", views.RetryClosurePDFView.as_view(), name="closure-pdf-retry"),
    path("closure-pdfs/<int:pk>/download/", views.DownloadClosurePDFView.as_view(), name="closure-pdf-download"),
]
