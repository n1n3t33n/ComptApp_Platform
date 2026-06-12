"""Vue : liste des partenaires avec filtre par type et recherche (nom, activité, ville)."""
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views import View

from partners.models import Partenaire


@method_decorator(login_required, name="dispatch")
class ListePartenairesView(View):

    template_name = "partners/crud/liste_partenaires.html"

    def get(self, request):
        qs = Partenaire.objects.all()
        type_filtre = request.GET.get("type", "")
        recherche = request.GET.get("q", "")

        if type_filtre in [Partenaire.Type.CLIENT, Partenaire.Type.FOURNISSEUR]:
            qs = qs.filter(type=type_filtre)
        if recherche:
            qs = qs.filter(
                Q(nom__icontains=recherche)
                | Q(activite__icontains=recherche)
                | Q(ville__icontains=recherche)
            )

        return render(
            request,
            self.template_name,
            {"partenaires": qs, "type_filtre": type_filtre, "recherche": recherche},
        )