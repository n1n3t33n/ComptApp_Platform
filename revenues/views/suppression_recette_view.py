"""Vue : suppression d'une recette (confirmation via POST)."""
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.decorators import method_decorator
from django.views import View

from revenues.models import Recette


@method_decorator(login_required, name="dispatch")
class SuppressionRecetteView(View):
    template_name = "revenues/confirmation_suppression.html"

    def get(self, request, pk):
        recette = get_object_or_404(Recette, pk=pk)
        return render(request, self.template_name, {"objet": recette})

    def post(self, request, pk):
        recette = get_object_or_404(Recette, pk=pk)
        recette.delete()
        messages.success(request, "Recette supprimée.")
        return redirect("revenues:liste_recettes")