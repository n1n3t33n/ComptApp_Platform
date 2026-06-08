"""Vue : liste des recettes avec recherche multi-critères."""
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views import View

from revenues.models import Recette


@method_decorator(login_required, name="dispatch")
class ListeRecettesView(View):
    template_name = "revenues/liste_recettes.html"

    def get(self, request):
        qs = Recette.objects.select_related("categorie", "partenaire", "saisi_par")

        recherche = request.GET.get("q", "")
        categorie = request.GET.get("categorie", "")
        date_debut = request.GET.get("date_debut", "")
        date_fin = request.GET.get("date_fin", "")

        if recherche:
            qs = qs.filter(description__icontains=recherche)
        if categorie:
            qs = qs.filter(categorie_id=categorie)
        if date_debut:
            qs = qs.filter(date__gte=date_debut)
        if date_fin:
            qs = qs.filter(date__lte=date_fin)

        total = qs.aggregate(total=Sum("montant"))["total"] or 0

        return render(
            request,
            self.template_name,
            {
                "recettes": qs,
                "total": total,
                "recherche": recherche,
                "date_debut": date_debut,
                "date_fin": date_fin,
            },
        )