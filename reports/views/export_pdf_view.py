"""
Vue : export PDF des rapports.

Logique métier : selon le paramètre `type` (journal, bilan, etats),
construit les données correspondantes et génère le PDF via le service dédié.
"""
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views import View

from reports.services import (
    construire_journal,
    construire_bilan,
    construire_etats,
    generer_pdf,
)


@method_decorator(login_required, name="dispatch")
class ExportPdfView(View):

    def get(self, request, type_rapport):
        date_debut = request.GET.get("date_debut", "") or None
        date_fin = request.GET.get("date_fin", "") or None
        aujourd_hui = timezone.localdate().isoformat()

        contexte_commun = {"date_debut": date_debut, "date_fin": date_fin}

        if type_rapport == "journal":
            contexte_commun["lignes"] = construire_journal(date_debut, date_fin)
            return generer_pdf(
                "reports/pdf/journal_pdf.html",
                contexte_commun,
                f"journal_{aujourd_hui}.pdf",
            )

        if type_rapport == "bilan":
            contexte_commun["bilan"] = construire_bilan(date_debut, date_fin)
            return generer_pdf(
                "reports/pdf/bilan_pdf.html",
                contexte_commun,
                f"bilan_{aujourd_hui}.pdf",
            )

        if type_rapport == "etats":
            contexte_commun["etats"] = construire_etats(date_debut, date_fin)
            return generer_pdf(
                "reports/pdf/etats_pdf.html",
                contexte_commun,
                f"etats_{aujourd_hui}.pdf",
            )

        raise Http404("Type de rapport inconnu.")