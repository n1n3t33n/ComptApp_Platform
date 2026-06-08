"""Package views de l'application revenues."""
from .liste_recettes_view import ListeRecettesView
from .ajout_recette_view import AjoutRecetteView
from .modification_recette_view import ModificationRecetteView
from .suppression_recette_view import SuppressionRecetteView

__all__ = [
    "ListeRecettesView",
    "AjoutRecetteView",
    "ModificationRecetteView",
    "SuppressionRecetteView",
]