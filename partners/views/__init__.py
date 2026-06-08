"""Package views de l'application partners."""
from .liste_partenaires_view import ListePartenairesView
from .ajout_partenaire_view import AjoutPartenaireView
from .modification_partenaire_view import ModificationPartenaireView
from .suppression_partenaire_view import SuppressionPartenaireView

__all__ = [
    "ListePartenairesView",
    "AjoutPartenaireView",
    "ModificationPartenaireView",
    "SuppressionPartenaireView",
]