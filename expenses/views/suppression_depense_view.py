"""Vue : suppression d'une dépense (confirmation via POST)."""
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.decorators import method_decorator
from django.views import View

from expenses.models import Depense


@method_decorator(login_required, name="dispatch")
class SuppressionDepenseView(View):
    template_name = "expenses/confirmation_suppression.html"

    def get(self, request, pk):
        depense = get_object_or_404(Depense, pk=pk)
        return render(request, self.template_name, {"objet": depense})

    def post(self, request, pk):
        depense = get_object_or_404(Depense, pk=pk)
        depense.delete()
        messages.success(request, "Dépense supprimée.")
        return redirect("expenses:liste_depenses")