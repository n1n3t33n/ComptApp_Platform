"""Formulaire de création / modification d'un partenaire."""
from django import forms

from partners.models import Partenaire


class PartenaireForm(forms.ModelForm):
    class Meta:
        model = Partenaire
        fields = ["type", "nom", "telephone", "adresse", "email"]
        widgets = {
            "adresse": forms.Textarea(attrs={"rows": 3}),
        }