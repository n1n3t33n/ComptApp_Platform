"""Vue : modification d'une recette existante."""
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.decorators import method_decorator
from django.views import View

from revenues.forms import RecetteForm
from revenues.models import Recette


@method_decorator(login_required, name="dispatch")
class ModificationRecetteView(View):
    template_name = "revenues/form_recette.html"

    def get(self, request, pk):
        recette = get_object_or_404(Recette, pk=pk)
        return render(
            request,
            self.template_name,
            {"form": RecetteForm(instance=recette), "action": "Modifier", "recette": recette},
        )

    def post(self, request, pk):
        recette = get_object_or_404(Recette, pk=pk)
        form = RecetteForm(request.POST, instance=recette)
        if form.is_valid():
            form.save()
            messages.success(request, "Recette modifiée avec succès.")
            return redirect("revenues:liste_recettes")
        return render(request, self.template_name, {"form": form, "action": "Modifier"})