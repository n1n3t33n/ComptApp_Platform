"""
Service OTP : logique métier de la double authentification.

Isolé ici pour pouvoir être réutilisé indépendamment des vues
(tests unitaires, future API, etc.).
"""
from django.conf import settings
from django.core.mail import send_mail

from accounts.models import ProfilOTP


def generer_et_envoyer_otp(utilisateur):
    """
    Génère un nouveau code OTP pour l'utilisateur et l'envoie par email.

    - Si un ProfilOTP existait, il est supprimé et remplacé
      (un seul code actif à la fois).
    - En développement, l'email s'affiche dans la console Django.
    """
    ProfilOTP.objects.filter(utilisateur=utilisateur).delete()
    profil_otp = ProfilOTP.objects.create(utilisateur=utilisateur)

    send_mail(
        subject="Votre code de vérification ComptApp Platform",
        message=(
            f"Bonjour {utilisateur.prenom},\n\n"
            f"Votre code de vérification est : {profil_otp.code_otp}\n\n"
            f"Ce code est valable {settings.OTP_VALIDITE_MINUTES} minutes.\n\n"
            f"Si vous n'êtes pas à l'origine de cette demande, ignorez cet email.\n\n"
            f"ComptApp Platform"
        ),
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[utilisateur.email],
        fail_silently=False,
    )
    return profil_otp


def valider_otp(utilisateur, code_saisi):
    """
    Vérifie le code OTP saisi.

    Retourne True si le code est correct, non expiré et non utilisé.
    Marque le code comme utilisé après validation (anti-replay).
    """
    try:
        profil_otp = ProfilOTP.objects.get(utilisateur=utilisateur)
    except ProfilOTP.DoesNotExist:
        return False

    if profil_otp.est_valide() and profil_otp.code_otp == code_saisi.strip():
        profil_otp.est_utilise = True
        profil_otp.save()
        return True

    return False