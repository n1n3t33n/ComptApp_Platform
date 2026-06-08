"""Routes de l'application reports."""
from django.urls import path

from reports.views import JournalView, BilanView, EtatsView, ExportPdfView

app_name = "reports"

urlpatterns = [
    path("journal/", JournalView.as_view(), name="journal"),
    path("bilan/", BilanView.as_view(), name="bilan"),
    path("etats/", EtatsView.as_view(), name="etats"),
    path("export/<str:type_rapport>/", ExportPdfView.as_view(), name="export_pdf"),
]