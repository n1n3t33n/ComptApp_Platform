"""Vue : ajout d'un nouveau partenaire (client ou fournisseur)."""
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.utils.decorators import method_decorator
from django.views import View

from partners.forms import PartenaireForm


@method_decorator(login_required, name="dispatch")
class AjoutPartenaireView(View):
    template_name = "partners/form_partenaire.html"

    def get(self, request):
        return render(
            request, self.template_name, {"form": PartenaireForm(), "action": "Ajouter"}
        )

    def post(self, request):
        form = PartenaireForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Partenaire ajouté avec succès.")
            return redirect("partners:liste_partenaires")
        return render(request, self.template_name, {"form": form, "action": "Ajouter"})