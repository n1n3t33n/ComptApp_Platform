"""Vue : modification d'une dépense existante."""
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.decorators import method_decorator
from django.views import View

from expenses.forms import DepenseForm
from expenses.models import Depense


@method_decorator(login_required, name="dispatch")
class ModificationDepenseView(View):
    
    template_name = "expenses/crud/form_depense.html"

    def get(self, request, pk):
        depense = get_object_or_404(Depense, pk=pk)
        return render(
            request,
            self.template_name,
            {"form": DepenseForm(instance=depense), "action": "Modifier", "depense": depense},
        )

    def post(self, request, pk):
        depense = get_object_or_404(Depense, pk=pk)
        form = DepenseForm(request.POST, instance=depense)
        if form.is_valid():
            form.save()
            messages.success(request, "Dépense modifiée avec succès.")
            return redirect("expenses:liste_depenses")
        return render(request, self.template_name, {"form": form, "action": "Modifier"})