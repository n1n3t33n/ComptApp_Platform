"""Vue : ajout d'une nouvelle recette."""
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.utils.decorators import method_decorator
from django.views import View

from revenues.forms import RecetteForm


@method_decorator(login_required, name="dispatch")
class AjoutRecetteView(View):
    template_name = "revenues/form_recette.html"

    def get(self, request):
        return render(
            request, self.template_name, {"form": RecetteForm(), "action": "Ajouter"}
        )

    def post(self, request):
        form = RecetteForm(request.POST)
        if form.is_valid():
            recette = form.save(commit=False)
            # Traçabilité : on affecte l'utilisateur connecté.
            recette.saisi_par = request.user
            recette.save()
            messages.success(request, "Recette enregistrée avec succès.")
            return redirect("revenues:liste_recettes")
        return render(request, self.template_name, {"form": form, "action": "Ajouter"})