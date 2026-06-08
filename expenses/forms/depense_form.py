"""Formulaire de création / modification d'une dépense."""
from django import forms

from expenses.models import Depense


class DepenseForm(forms.ModelForm):
    class Meta:
        model = Depense
        # saisi_par affecté automatiquement à l'utilisateur connecté dans la vue.
        fields = ["date", "montant", "description", "partenaire", "categorie"]
        widgets = {
            "date": forms.DateInput(attrs={"type": "date"}),
            "description": forms.Textarea(attrs={"rows": 3}),
        }