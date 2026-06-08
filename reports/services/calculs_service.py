"""
Service de calculs comptables.

Centralise toute la logique métier des rapports : journal, bilan simplifié
et états par catégorie. Aucune écriture en base — uniquement de la lecture
et de l'agrégation. Isolé des vues pour être testable et réutilisable
(les vues HTML et l'export PDF s'appuient tous deux dessus).
"""
from django.db.models import Sum

from revenues.models import Recette
from expenses.models import Depense


def _filtrer_periode(qs, date_debut, date_fin):
    """Applique un filtre de plage de dates si fourni."""
    if date_debut:
        qs = qs.filter(date__gte=date_debut)
    if date_fin:
        qs = qs.filter(date__lte=date_fin)
    return qs


def construire_journal(date_debut=None, date_fin=None):
    """
    Journal des opérations : liste chronologique unifiée des recettes et
    dépenses, chacune marquée par son sens. Trié par date croissante.

    Retourne une liste de dictionnaires homogènes prêts à afficher.
    """
    recettes = _filtrer_periode(
        Recette.objects.select_related("categorie", "partenaire"), date_debut, date_fin
    )
    depenses = _filtrer_periode(
        Depense.objects.select_related("categorie", "partenaire"), date_debut, date_fin
    )

    lignes = []
    for r in recettes:
        lignes.append({
            "date": r.date,
            "sens": "Recette",
            "description": r.description,
            "categorie": r.categorie.libelle,
            "partenaire": r.partenaire.nom if r.partenaire else "—",
            "recette": r.montant,
            "depense": None,
        })
    for d in depenses:
        lignes.append({
            "date": d.date,
            "sens": "Dépense",
            "description": d.description,
            "categorie": d.categorie.libelle,
            "partenaire": d.partenaire.nom if d.partenaire else "—",
            "recette": None,
            "depense": d.montant,
        })

    # Tri chronologique (date croissante)
    lignes.sort(key=lambda ligne: ligne["date"])
    return lignes


def construire_bilan(date_debut=None, date_fin=None):
    """
    Bilan simplifié : total des recettes, total des dépenses et solde net
    (résultat) sur la période. Le solde positif = bénéfice, négatif = perte.
    """
    total_recettes = (
        _filtrer_periode(Recette.objects.all(), date_debut, date_fin)
        .aggregate(total=Sum("montant"))["total"] or 0
    )
    total_depenses = (
        _filtrer_periode(Depense.objects.all(), date_debut, date_fin)
        .aggregate(total=Sum("montant"))["total"] or 0
    )
    solde = total_recettes - total_depenses

    return {
        "total_recettes": total_recettes,
        "total_depenses": total_depenses,
        "solde": solde,
        "resultat": "Bénéfice" if solde >= 0 else "Perte",
    }


def construire_etats(date_debut=None, date_fin=None):
    """
    États détaillés par catégorie : ventile les recettes et les dépenses
    par catégorie comptable, avec sous-totaux. Permet de voir la répartition
    (ex : combien en Salaires, en Loyer, en Ventes...).
    """
    recettes_par_cat = (
        _filtrer_periode(Recette.objects.all(), date_debut, date_fin)
        .values("categorie__libelle")
        .annotate(total=Sum("montant"))
        .order_by("-total")
    )
    depenses_par_cat = (
        _filtrer_periode(Depense.objects.all(), date_debut, date_fin)
        .values("categorie__libelle")
        .annotate(total=Sum("montant"))
        .order_by("-total")
    )
    return {
        "recettes_par_categorie": list(recettes_par_cat),
        "depenses_par_categorie": list(depenses_par_cat),
    }