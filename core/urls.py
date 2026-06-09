"""Routes de l'application core."""
from django.urls import path
from django.views.generic import RedirectView
from core.views import tableau_de_bord_view, SauvegardeView

app_name = "core"

urlpatterns = [
    # La racine redirige vers le tableau de bord (qui exige la connexion)
    path("", RedirectView.as_view(pattern_name="core:tableau_de_bord"), name="accueil"),
    path("tableau-de-bord/", tableau_de_bord_view, name="tableau_de_bord"),
    path("sauvegarde/", SauvegardeView.as_view(), name="sauvegarde"),
]