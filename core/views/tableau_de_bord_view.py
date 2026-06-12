"""
Vue : Tableau de bord principal.

Logique métier : agrégation des chiffres clés du mois en cours pour
donner une vision instantanée à l'utilisateur, plus les séries de
données alimentant les graphiques (évolution sur 6 mois, répartition
des dépenses par catégorie). Accessible uniquement aux utilisateurs
authentifiés ayant passé la 2FA.
"""
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.db.models.functions import TruncMonth
from django.shortcuts import render
from django.utils import timezone

from revenues.models import Recette
from expenses.models import Depense

MOIS_FRANCAIS = ["Jan", "Fév", "Mar", "Avr", "Mai", "Juin",
                 "Juil", "Août", "Sep", "Oct", "Nov", "Déc"]
MOIS_FRANCAIS_COMPLETS = ["janvier", "février", "mars", "avril", "mai", "juin",
                          "juillet", "août", "septembre", "octobre", "novembre", "décembre"]
NOMBRE_MOIS_GRAPHIQUE = 6


def _premier_jour_mois_decale(date_reference, decalage):
    """Premier jour du mois situé `decalage` mois avant la date de référence."""
    annee, mois = date_reference.year, date_reference.month - decalage
    while mois <= 0:
        mois += 12
        annee -= 1
    return date_reference.replace(year=annee, month=mois, day=1)


def _totaux_par_mois(queryset, date_debut):
    """Agrège les montants d'un queryset par mois : {(année, mois): total}."""
    lignes = (
        queryset.filter(date__gte=date_debut)
        .annotate(mois=TruncMonth("date"))
        .values("mois")
        .annotate(total=Sum("montant"))
    )
    return {(l["mois"].year, l["mois"].month): float(l["total"]) for l in lignes}


def _variation_pourcentage(actuel, precedent):
    """Variation en % par rapport au mois précédent (None si pas de référence)."""
    if precedent:
        return round((actuel - precedent) / precedent * 100, 1)
    return None


@login_required
def tableau_de_bord_view(request):
    """
    Affiche le tableau de bord avec les indicateurs du mois en cours
    (totaux, variations vs mois précédent, trésorerie cumulée), les
    graphiques d'évolution et de répartition, et les dernières opérations.
    """
    aujourd_hui = timezone.localdate()
    debut_mois = aujourd_hui.replace(day=1)
    debut_mois_precedent = _premier_jour_mois_decale(aujourd_hui, 1)

    recettes_mois = (
        Recette.objects.filter(date__gte=debut_mois)
        .aggregate(total=Sum("montant"))["total"] or 0
    )
    depenses_mois = (
        Depense.objects.filter(date__gte=debut_mois)
        .aggregate(total=Sum("montant"))["total"] or 0
    )
    solde_net = recettes_mois - depenses_mois

    # Mois précédent : sert à afficher la tendance sur les cartes
    recettes_mois_precedent = (
        Recette.objects.filter(date__gte=debut_mois_precedent, date__lt=debut_mois)
        .aggregate(total=Sum("montant"))["total"] or 0
    )
    depenses_mois_precedent = (
        Depense.objects.filter(date__gte=debut_mois_precedent, date__lt=debut_mois)
        .aggregate(total=Sum("montant"))["total"] or 0
    )

    # Trésorerie cumulée depuis le début de l'activité
    total_recettes_global = Recette.objects.aggregate(total=Sum("montant"))["total"] or 0
    total_depenses_global = Depense.objects.aggregate(total=Sum("montant"))["total"] or 0
    tresorerie_totale = total_recettes_global - total_depenses_global

    # Série mensuelle pour la courbe d'évolution
    debut_periode = _premier_jour_mois_decale(aujourd_hui, NOMBRE_MOIS_GRAPHIQUE - 1)
    recettes_par_mois = _totaux_par_mois(Recette.objects.all(), debut_periode)
    depenses_par_mois = _totaux_par_mois(Depense.objects.all(), debut_periode)

    labels_mois, serie_recettes, serie_depenses = [], [], []
    for decalage in range(NOMBRE_MOIS_GRAPHIQUE - 1, -1, -1):
        mois = _premier_jour_mois_decale(aujourd_hui, decalage)
        labels_mois.append(f"{MOIS_FRANCAIS[mois.month - 1]} {str(mois.year)[2:]}")
        serie_recettes.append(recettes_par_mois.get((mois.year, mois.month), 0.0))
        serie_depenses.append(depenses_par_mois.get((mois.year, mois.month), 0.0))

    # Solde net mensuel (barres vertes/rouges)
    serie_solde = [r - d for r, d in zip(serie_recettes, serie_depenses)]

    # Répartition des dépenses du mois par catégorie (graphique en anneau)
    depenses_categories = (
        Depense.objects.filter(date__gte=debut_mois)
        .values("categorie__libelle")
        .annotate(total=Sum("montant"))
        .order_by("-total")
    )
    # Répartition des recettes du mois par catégorie (graphique en anneau)
    recettes_categories = (
        Recette.objects.filter(date__gte=debut_mois)
        .values("categorie__libelle")
        .annotate(total=Sum("montant"))
        .order_by("-total")
    )

    dernieres_recettes = (
        Recette.objects.select_related("categorie", "partenaire")
        .order_by("-date_saisie")[:5]
    )
    dernieres_depenses = (
        Depense.objects.select_related("categorie", "partenaire")
        .order_by("-date_saisie")[:5]
    )

    context = {
        "recettes_mois": recettes_mois,
        "depenses_mois": depenses_mois,
        "solde_net": solde_net,
        "tresorerie_totale": tresorerie_totale,
        "variation_recettes": _variation_pourcentage(
            float(recettes_mois), float(recettes_mois_precedent)
        ),
        "variation_depenses": _variation_pourcentage(
            float(depenses_mois), float(depenses_mois_precedent)
        ),
        "graphique_evolution": {
            "labels": labels_mois,
            "recettes": serie_recettes,
            "depenses": serie_depenses,
        },
        "graphique_categories": {
            "labels": [l["categorie__libelle"] for l in depenses_categories],
            "valeurs": [float(l["total"]) for l in depenses_categories],
        },
        "graphique_recettes_categories": {
            "labels": [l["categorie__libelle"] for l in recettes_categories],
            "valeurs": [float(l["total"]) for l in recettes_categories],
        },
        "graphique_solde_mensuel": {
            "labels": labels_mois,
            "valeurs": serie_solde,
        },
        "dernieres_recettes": dernieres_recettes,
        "dernieres_depenses": dernieres_depenses,
        "mois_courant": f"{MOIS_FRANCAIS_COMPLETS[aujourd_hui.month - 1]} {aujourd_hui.year}",
    }
    return render(request, "core/dashboard/tableau_de_bord.html", context)
