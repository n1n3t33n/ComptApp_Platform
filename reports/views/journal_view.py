"""Vue : journal chronologique des opérations."""
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views import View

from reports.services import construire_journal


@method_decorator(login_required, name="dispatch")
class JournalView(View):
    template_name = "reports/ecran/journal.html"

    def get(self, request):
        date_debut = request.GET.get("date_debut", "")
        date_fin = request.GET.get("date_fin", "")
        lignes = construire_journal(date_debut or None, date_fin or None)

        # Totaux de la période (pied du tableau)
        total_recettes = sum(l["recette"] or 0 for l in lignes)
        total_depenses = sum(l["depense"] or 0 for l in lignes)

        # Courbe de trésorerie : solde cumulé opération après opération
        labels, valeurs, solde_cumule = [], [], 0
        for ligne in lignes:
            solde_cumule += (ligne["recette"] or 0) - (ligne["depense"] or 0)
            labels.append(ligne["date"].strftime("%d/%m/%Y"))
            valeurs.append(float(solde_cumule))

        return render(
            request,
            self.template_name,
            {
                "lignes": lignes,
                "total_recettes": total_recettes,
                "total_depenses": total_depenses,
                "solde_periode": total_recettes - total_depenses,
                "graphique_solde": {"labels": labels, "valeurs": valeurs},
                "date_debut": date_debut,
                "date_fin": date_fin,
            },
        )
