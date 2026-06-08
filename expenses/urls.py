"""Routes de l'application expenses."""
from django.urls import path

from expenses.views import (
    ListeDepensesView,
    AjoutDepenseView,
    ModificationDepenseView,
    SuppressionDepenseView,
)

app_name = "expenses"

urlpatterns = [
    path("", ListeDepensesView.as_view(), name="liste_depenses"),
    path("ajouter/", AjoutDepenseView.as_view(), name="ajout_depense"),
    path("<int:pk>/modifier/", ModificationDepenseView.as_view(), name="modification_depense"),
    path("<int:pk>/supprimer/", SuppressionDepenseView.as_view(), name="suppression_depense"),
]