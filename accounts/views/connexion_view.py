"""
Vue : Connexion (étape 1 de la 2FA).

Logique métier : vérifie email + mot de passe. Si corrects, stocke l'ID
de l'utilisateur en session (sans l'authentifier complètement) et déclenche
l'envoi du code OTP. L'authentification complète n'a lieu qu'après validation
du code OTP (étape 2).
"""
from django.contrib.auth import authenticate
from django.shortcuts import redirect, render
from django.views import View

from accounts.forms import ConnexionForm
from accounts.services import generer_et_envoyer_otp


class ConnexionView(View):
    """Étape 1 de la 2FA : saisie des identifiants."""

    template_name = "accounts/auth/connexion.html"

    def get(self, request):
        if request.user.is_authenticated:
            return redirect("core:tableau_de_bord")
        return render(request, self.template_name, {"form": ConnexionForm()})

    def post(self, request):
        form = ConnexionForm(request.POST)
        if not form.is_valid():
            return render(request, self.template_name, {"form": form})

        email = form.cleaned_data["email"]
        password = form.cleaned_data["password"]
        utilisateur = authenticate(request, username=email, password=password)

        if utilisateur is None:
            form.add_error(None, "Email ou mot de passe incorrect.")
            return render(request, self.template_name, {"form": form})

        if not utilisateur.is_active:
            form.add_error(None, "Ce compte est désactivé. Contactez l'administrateur.")
            return render(request, self.template_name, {"form": form})

        # Stocke l'ID en session pour l'étape 2 (sans login complet)
        request.session["otp_user_id"] = utilisateur.pk
        # Génère et envoie le code OTP (affiché dans la console en dev)
        generer_et_envoyer_otp(utilisateur)

        return redirect("accounts:verification_otp")