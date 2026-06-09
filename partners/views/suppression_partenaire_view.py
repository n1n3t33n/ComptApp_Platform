"""Vue : suppression d'un partenaire (confirmation requise via POST)."""
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.decorators import method_decorator
from django.views import View

from partners.models import Partenaire


@method_decorator(login_required, name="dispatch")
class SuppressionPartenaireView(View):
    
    template_name = "partners/crud/confirmation_suppression.html"

    def get(self, request, pk):
        partenaire = get_object_or_404(Partenaire, pk=pk)
        return render(request, self.template_name, {"objet": partenaire})

    def post(self, request, pk):
        partenaire = get_object_or_404(Partenaire, pk=pk)
        partenaire.delete()
        messages.success(request, "Partenaire supprimé.")
        return redirect("partners:liste_partenaires")