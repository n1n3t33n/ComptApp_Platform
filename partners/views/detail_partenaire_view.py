"""
Vue : fiche détaillée d'un partenaire avec historique complet des transactions.

Regroupe, pour un client ou un fournisseur donné, l'intégralité de ses
opérations (recettes s'il est client, dépenses s'il est fournisseur),
présentées comme un relevé chronologique avec solde cumulé, des totaux
de synthèse et un graphique d'évolution mensuelle.
"""
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.shortcuts import get_object_or_404, render
from django.utils.decorators import method_decorator
from django.views import View

from partners.models import Partenaire

MOIS_FRANCAIS = ["Jan", "Fév", "Mar", "Avr", "Mai", "Juin",
                 "Juil", "Août", "Sep", "Oct", "Nov", "Déc"]


@method_decorator(login_required, name="dispatch")
class DetailPartenaireView(View):
    template_name = "partners/crud/detail_partenaire.html"

    def get(self, request, pk):
        partenaire = get_object_or_404(Partenaire, pk=pk)

        recettes = partenaire.recettes.select_related("categorie")
        depenses = partenaire.depenses.select_related("categorie")

        # Relevé unifié, chaque ligne marquée par son sens
        operations = []
        for r in recettes:
            operations.append({
                "date": r.date,
                "sens": "Recette",
                "description": r.description,
                "categorie": r.categorie.libelle,
                "recette": r.montant,
                "depense": None,
            })
        for d in depenses:
            operations.append({
                "date": d.date,
                "sens": "Dépense",
                "description": d.description,
                "categorie": d.categorie.libelle,
                "recette": None,
                "depense": d.montant,
            })
        operations.sort(key=lambda o: o["date"])

        # Solde cumulé opération après opération (pour la colonne et la courbe)
        cumul = 0
        labels_courbe, valeurs_courbe = [], []
        for op in operations:
            cumul += (op["recette"] or 0) - (op["depense"] or 0)
            op["solde_cumule"] = cumul
            labels_courbe.append(op["date"].strftime("%d/%m/%Y"))
            valeurs_courbe.append(float(cumul))

        total_recettes = recettes.aggregate(t=Sum("montant"))["t"] or 0
        total_depenses = depenses.aggregate(t=Sum("montant"))["t"] or 0

        # Volume mensuel des transactions (12 derniers mois représentés)
        graphique_mensuel = self._volume_mensuel(operations)

        context = {
            "partenaire": partenaire,
            "operations": operations,
            "nb_operations": len(operations),
            "total_recettes": total_recettes,
            "total_depenses": total_depenses,
            "solde": total_recettes - total_depenses,
            "graphique_solde": {"labels": labels_courbe, "valeurs": valeurs_courbe},
            "graphique_mensuel": graphique_mensuel,
        }
        return render(request, self.template_name, context)

    @staticmethod
    def _volume_mensuel(operations):
        """Agrège recettes et dépenses par mois (clé 'MMM AA') pour un graphique barres."""
        par_mois = {}
        ordre = []
        for op in operations:
            cle = (op["date"].year, op["date"].month)
            if cle not in par_mois:
                par_mois[cle] = {"recette": 0.0, "depense": 0.0}
                ordre.append(cle)
            par_mois[cle]["recette"] += float(op["recette"] or 0)
            par_mois[cle]["depense"] += float(op["depense"] or 0)

        ordre.sort()
        return {
            "labels": [f"{MOIS_FRANCAIS[m - 1]} {str(a)[2:]}" for (a, m) in ordre],
            "recettes": [par_mois[c]["recette"] for c in ordre],
            "depenses": [par_mois[c]["depense"] for c in ordre],
        }
