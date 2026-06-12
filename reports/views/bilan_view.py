"""Vue : bilan simplifié."""
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views import View

from reports.services import construire_bilan


@method_decorator(login_required, name="dispatch")
class BilanView(View):

    template_name = "reports/ecran/bilan.html"

    def get(self, request):
        date_debut = request.GET.get("date_debut", "")
        date_fin = request.GET.get("date_fin", "")
        bilan = construire_bilan(date_debut or None, date_fin or None)

        # Données du graphique comparatif (barres recettes / dépenses / solde)
        graphique_bilan = {
            "recettes": float(bilan["total_recettes"]),
            "depenses": float(bilan["total_depenses"]),
            "solde": float(bilan["solde"]),
        }

        # Part des recettes consommée par les dépenses (jauge de l'interprétation)
        if graphique_bilan["recettes"] > 0:
            taux_charges = round(
                graphique_bilan["depenses"] / graphique_bilan["recettes"] * 100, 1
            )
        else:
            taux_charges = None

        return render(
            request,
            self.template_name,
            {
                "bilan": bilan,
                "graphique_bilan": graphique_bilan,
                "taux_charges": taux_charges,
                "date_debut": date_debut,
                "date_fin": date_fin,
            },
        )
