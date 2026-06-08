"""Formulaire de création / modification d'une recette."""
from django import forms

from revenues.models import Recette


class RecetteForm(forms.ModelForm):
    class Meta:
        model = Recette
        # saisi_par n'est PAS dans le formulaire : il est affecté
        # automatiquement à l'utilisateur connecté dans la vue.
        fields = ["date", "montant", "description", "partenaire", "categorie"]
        widgets = {
            "date": forms.DateInput(attrs={"type": "date"}),
            "description": forms.Textarea(attrs={"rows": 3}),
        }