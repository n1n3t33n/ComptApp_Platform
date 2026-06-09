"""
Vue : Vérification OTP (étape 2 de la 2FA).

Logique métier : récupère l'utilisateur mis en session à l'étape 1,
vérifie le code OTP saisi, puis connecte réellement l'utilisateur
(login Django) si le code est valide.
"""
from django.contrib.auth import get_user_model, login
from django.shortcuts import redirect, render
from django.views import View

from accounts.forms import VerificationOtpForm
from accounts.services import valider_otp

Utilisateur = get_user_model()


class VerificationOtpView(View):
    """Étape 2 de la 2FA : saisie du code OTP."""

    template_name = "accounts/auth/verification_otp.html"

    def _get_utilisateur(self, request):
        user_id = request.session.get("otp_user_id")
        if not user_id:
            return None
        try:
            return Utilisateur.objects.get(pk=user_id)
        except Utilisateur.DoesNotExist:
            return None

    def get(self, request):
        if not self._get_utilisateur(request):
            return redirect("accounts:connexion")
        return render(request, self.template_name, {"form": VerificationOtpForm()})

    def post(self, request):
        utilisateur = self._get_utilisateur(request)
        if not utilisateur:
            return redirect("accounts:connexion")

        form = VerificationOtpForm(request.POST)
        if not form.is_valid():
            return render(request, self.template_name, {"form": form})

        code_saisi = form.cleaned_data["code_otp"]
        if valider_otp(utilisateur, code_saisi):
            del request.session["otp_user_id"]
            login(
                request,
                utilisateur,
                backend="django.contrib.auth.backends.ModelBackend",
            )
            return redirect("core:tableau_de_bord")

        form.add_error("code_otp", "Code incorrect ou expiré. Veuillez recommencer.")
        return render(request, self.template_name, {"form": form})