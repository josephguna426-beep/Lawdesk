from django.urls import path

from . import views

urlpatterns = [
    path("search/", views.GlobalSearchView.as_view(), name="report-search"),
    path("case-status/", views.CaseStatusReportView.as_view(), name="report-case-status"),
    path("upcoming-hearings/", views.UpcomingHearingsReportView.as_view(), name="report-upcoming-hearings"),
]
