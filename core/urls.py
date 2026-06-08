"""Routes de l'application core."""
from django.urls import path
from core.views import tableau_de_bord_view

app_name = "core"

urlpatterns = [
    path("tableau-de-bord/", tableau_de_bord_view, name="tableau_de_bord"),
]