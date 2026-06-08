"""Routes de l'application revenues."""
from django.urls import path

from revenues.views import (
    ListeRecettesView,
    AjoutRecetteView,
    ModificationRecetteView,
    SuppressionRecetteView,
)

app_name = "revenues"

urlpatterns = [
    path("", ListeRecettesView.as_view(), name="liste_recettes"),
    path("ajouter/", AjoutRecetteView.as_view(), name="ajout_recette"),
    path("<int:pk>/modifier/", ModificationRecetteView.as_view(), name="modification_recette"),
    path("<int:pk>/supprimer/", SuppressionRecetteView.as_view(), name="suppression_recette"),
]