"""Vue : journal chronologique des opérations."""
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views import View

from reports.services import construire_journal


@method_decorator(login_required, name="dispatch")
class JournalView(View):
    template_name = "reports/journal.html"

    def get(self, request):
        date_debut = request.GET.get("date_debut", "")
        date_fin = request.GET.get("date_fin", "")
        lignes = construire_journal(date_debut or None, date_fin or None)
        return render(
            request,
            self.template_name,
            {"lignes": lignes, "date_debut": date_debut, "date_fin": date_fin},
        )