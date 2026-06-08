"""Vue : états détaillés par catégorie."""
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views import View

from reports.services import construire_etats


@method_decorator(login_required, name="dispatch")
class EtatsView(View):
    template_name = "reports/etats.html"

    def get(self, request):
        date_debut = request.GET.get("date_debut", "")
        date_fin = request.GET.get("date_fin", "")
        etats = construire_etats(date_debut or None, date_fin or None)
        return render(
            request,
            self.template_name,
            {"etats": etats, "date_debut": date_debut, "date_fin": date_fin},
        )