"""Formulaire de saisie du code OTP (étape 2 : vérification 2FA)."""
from django import forms


class VerificationOtpForm(forms.Form):
    code_otp = forms.CharField(
        label="Code de vérification",
        max_length=6,
        min_length=6,
        widget=forms.TextInput(
            attrs={
                "placeholder": "______",
                "autocomplete": "one-time-code",
                "inputmode": "numeric",
                "autofocus": True,
            }
        ),
    )

    def clean_code_otp(self):
        code = self.cleaned_data.get("code_otp", "")
        if not code.isdigit():
            raise forms.ValidationError("Le code doit contenir uniquement des chiffres.")
        return code