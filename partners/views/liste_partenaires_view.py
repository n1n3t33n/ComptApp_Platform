"""Vue : liste des partenaires avec filtre par type et recherche par nom."""
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views import View

from partners.models import Partenaire


@method_decorator(login_required, name="dispatch")
class ListePartenairesView(View):
    template_name = "partners/liste_partenaires.html"

    def get(self, request):
        qs = Partenaire.objects.all()
        type_filtre = request.GET.get("type", "")
        recherche = request.GET.get("q", "")

        if type_filtre in [Partenaire.Type.CLIENT, Partenaire.Type.FOURNISSEUR]:
            qs = qs.filter(type=type_filtre)
        if recherche:
            qs = qs.filter(nom__icontains=recherche)

        return render(
            request,
            self.template_name,
            {"partenaires": qs, "type_filtre": type_filtre, "recherche": recherche},
        )