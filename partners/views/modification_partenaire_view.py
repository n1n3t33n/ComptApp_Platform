"""Vue : modification d'un partenaire existant."""
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.decorators import method_decorator
from django.views import View

from partners.forms import PartenaireForm
from partners.models import Partenaire


@method_decorator(login_required, name="dispatch")
class ModificationPartenaireView(View):
    template_name = "partners/crud/form_partenaire.html"

    def get(self, request, pk):
        partenaire = get_object_or_404(Partenaire, pk=pk)
        return render(
            request,
            self.template_name,
            {
                "form": PartenaireForm(instance=partenaire),
                "action": "Modifier",
                "partenaire": partenaire,
            },
        )

    def post(self, request, pk):
        partenaire = get_object_or_404(Partenaire, pk=pk)
        form = PartenaireForm(request.POST, instance=partenaire)
        if form.is_valid():
            form.save()
            messages.success(request, "Partenaire modifié avec succès.")
            return redirect("partners:liste_partenaires")
        return render(request, self.template_name, {"form": form, "action": "Modifier"})