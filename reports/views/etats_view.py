"""Vue : états détaillés par catégorie."""
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views import View

from reports.services import construire_etats


def _enrichir_pourcentages(lignes):
    """Ajoute à chaque ligne sa part (%) du total, pour les barres de progression."""
    total = sum(float(ligne["total"]) for ligne in lignes)
    for ligne in lignes:
        ligne["pourcentage"] = round(float(ligne["total"]) / total * 100, 1) if total else 0.0
    return lignes


def _donnees_anneau(lignes):
    """Transforme les lignes par catégorie en données pour un graphique en anneau."""
    return {
        "labels": [ligne["categorie__libelle"] for ligne in lignes],
        "valeurs": [float(ligne["total"]) for ligne in lignes],
    }


@method_decorator(login_required, name="dispatch")
class EtatsView(View):

    template_name = "reports/ecran/etats.html"

    def get(self, request):
        date_debut = request.GET.get("date_debut", "")
        date_fin = request.GET.get("date_fin", "")
        etats = construire_etats(date_debut or None, date_fin or None)

        _enrichir_pourcentages(etats["recettes_par_categorie"])
        _enrichir_pourcentages(etats["depenses_par_categorie"])

        return render(
            request,
            self.template_name,
            {
                "etats": etats,
                "graphique_recettes": _donnees_anneau(etats["recettes_par_categorie"]),
                "graphique_depenses": _donnees_anneau(etats["depenses_par_categorie"]),
                "date_debut": date_debut,
                "date_fin": date_fin,
            },
        )
