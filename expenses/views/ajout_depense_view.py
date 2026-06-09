"""Vue : ajout d'une nouvelle dépense."""
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.utils.decorators import method_decorator
from django.views import View

from expenses.forms import DepenseForm


@method_decorator(login_required, name="dispatch")
class AjoutDepenseView(View):
    
    template_name = "expenses/crud/form_depense.html"

    def get(self, request):
        return render(
            request, self.template_name, {"form": DepenseForm(), "action": "Ajouter"}
        )

    def post(self, request):
        form = DepenseForm(request.POST)
        if form.is_valid():
            depense = form.save(commit=False)
            depense.saisi_par = request.user
            depense.save()
            messages.success(request, "Dépense enregistrée avec succès.")
            return redirect("expenses:liste_depenses")
        return render(request, self.template_name, {"form": form, "action": "Ajouter"})