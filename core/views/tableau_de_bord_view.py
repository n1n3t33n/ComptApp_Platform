"""
Vue : Tableau de bord principal.

Logique métier : agrégation des chiffres clés du mois en cours pour
donner une vision instantanée à l'utilisateur. Accessible uniquement
aux utilisateurs authentifiés ayant passé la 2FA.
"""
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.shortcuts import render
from django.utils import timezone

from revenues.models import Recette
from expenses.models import Depense


@login_required
def tableau_de_bord_view(request):
    """
    Affiche le tableau de bord avec les indicateurs du mois en cours :
    total recettes, total dépenses, solde net, et dernières opérations.
    """
    aujourd_hui = timezone.localdate()
    debut_mois = aujourd_hui.replace(day=1)

    recettes_mois = (
        Recette.objects.filter(date__gte=debut_mois)
        .aggregate(total=Sum("montant"))["total"] or 0
    )
    depenses_mois = (
        Depense.objects.filter(date__gte=debut_mois)
        .aggregate(total=Sum("montant"))["total"] or 0
    )
    solde_net = recettes_mois - depenses_mois

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
        "dernieres_recettes": dernieres_recettes,
        "dernieres_depenses": dernieres_depenses,
        "mois_courant": aujourd_hui.strftime("%B %Y"),
    }
    return render(request, "core/dashboard/tableau_de_bord.html", context)