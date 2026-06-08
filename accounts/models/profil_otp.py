"""
Modèle ProfilOTP.

Logique métier : à chaque tentative de connexion valide, un code OTP à
6 chiffres est généré, stocké ici avec une date d'expiration, puis envoyé
par email. L'utilisateur dispose de OTP_VALIDITE_MINUTES minutes pour le
saisir. Après validation, est_utilise passe à True pour empêcher la
réutilisation du même code (protection anti-replay).
"""
import random
from datetime import timedelta

from django.conf import settings
from django.db import models
from django.utils import timezone


class ProfilOTP(models.Model):
    """
    Code OTP temporaire lié à un utilisateur pour la double authentification.

    Contraintes métier :
    - Un seul ProfilOTP par utilisateur (OneToOneField).
    - Le code expire après OTP_VALIDITE_MINUTES minutes.
    - Un code déjà utilisé ne peut pas être réutilisé.
    """

    utilisateur = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="profil_otp",
        verbose_name="Utilisateur",
    )
    code_otp = models.CharField(max_length=6, verbose_name="Code OTP")
    date_creation = models.DateTimeField(auto_now_add=True)
    date_expiration = models.DateTimeField(verbose_name="Expiration")
    est_utilise = models.BooleanField(default=False, verbose_name="Utilisé")

    class Meta:
        app_label = "accounts"
        verbose_name = "Profil OTP"

    def __str__(self):
        return f"OTP de {self.utilisateur.email}"

    def save(self, *args, **kwargs):
        """Génère automatiquement le code et l'expiration à la création."""
        if not self.pk:
            self.code_otp = f"{random.randint(0, 999999):06d}"
            validite = getattr(settings, "OTP_VALIDITE_MINUTES", 5)
            self.date_expiration = timezone.now() + timedelta(minutes=validite)
        super().save(*args, **kwargs)

    def est_valide(self):
        """True si le code n'est ni expiré ni déjà utilisé."""
        return not self.est_utilise and timezone.now() <= self.date_expiration