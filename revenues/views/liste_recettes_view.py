"""Vue : liste des recettes avec recherche multi-critères."""
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views import View

from core.models import CategorieOperation
from revenues.models import Recette


@method_decorator(login_required, name="dispatch")
class ListeRecettesView(View):

    template_name = "revenues/crud/liste_recettes.html"

    def get(self, request):
        qs = Recette.objects.select_related("categorie", "partenaire", "saisi_par")

        recherche = request.GET.get("q", "")
        categorie_id = request.GET.get("categorie", "")
        date_debut = request.GET.get("date_debut", "")
        date_fin = request.GET.get("date_fin", "")

        if recherche:
            qs = qs.filter(description__icontains=recherche)
        if categorie_id:
            qs = qs.filter(categorie_id=categorie_id)
        if date_debut:
            qs = qs.filter(date__gte=date_debut)
        if date_fin:
            qs = qs.filter(date__lte=date_fin)

        total = qs.aggregate(total=Sum("montant"))["total"] or 0
        categories = CategorieOperation.objects.filter(sens=CategorieOperation.Sens.RECETTE)

        return render(
            request,
            self.template_name,
            {
                "recettes": qs,
                "total": total,
                "recherche": recherche,
                "categorie_id": categorie_id,
                "date_debut": date_debut,
                "date_fin": date_fin,
                "categories": categories,
            },
        )