"""Formulaire de connexion (étape 1 : email + mot de passe)."""
from django import forms


class ConnexionForm(forms.Form):
    email = forms.EmailField(
        label="Adresse email",
        widget=forms.EmailInput(
            attrs={"placeholder": "votre@email.com", "autofocus": True}
        ),
    )
    password = forms.CharField(
        label="Mot de passe",
        widget=forms.PasswordInput(attrs={"placeholder": "••••••••"}),
    )