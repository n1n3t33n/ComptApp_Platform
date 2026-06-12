"""Routes de l'application partners."""
from django.urls import path

from partners.views import (
    ListePartenairesView,
    DetailPartenaireView,
    AjoutPartenaireView,
    ModificationPartenaireView,
    SuppressionPartenaireView,
)

app_name = "partners"

urlpatterns = [
    path("", ListePartenairesView.as_view(), name="liste_partenaires"),
    path("ajouter/", AjoutPartenaireView.as_view(), name="ajout_partenaire"),
    path("<int:pk>/", DetailPartenaireView.as_view(), name="detail_partenaire"),
    path("<int:pk>/modifier/", ModificationPartenaireView.as_view(), name="modification_partenaire"),
    path("<int:pk>/supprimer/", SuppressionPartenaireView.as_view(), name="suppression_partenaire"),
]