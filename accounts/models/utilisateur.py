"""
Modèle Utilisateur (CustomUser).

Logique métier : on substitue le modèle User de Django par notre propre
modèle dès le départ (AUTH_USER_MODEL = 'accounts.Utilisateur').
L'identifiant de connexion est l'EMAIL (et non le username).
Les deux rôles possibles sont ADMIN et AGENT (comptable).
"""
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.db import models


class UtilisateurManager(BaseUserManager):
    """Gestionnaire personnalisé : l'email remplace le username."""

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("L'adresse email est obligatoire.")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("role", Utilisateur.Role.ADMIN)
        return self.create_user(email, password, **extra_fields)


class Utilisateur(AbstractBaseUser, PermissionsMixin):
    """
    Utilisateur de ComptApp Platform.

    - ADMIN : accès complet, gestion des comptes, sauvegarde/restauration.
    - AGENT : saisie des opérations, gestion des partenaires, rapports.
    - La création de compte se fait UNIQUEMENT via l'admin Django.
    - La connexion sur le site utilise email + mot de passe + OTP (2FA).
    """

    class Role(models.TextChoices):
        ADMIN = "ADMIN", "Administrateur"
        AGENT = "AGENT", "Agent comptable"

    email = models.EmailField(unique=True, verbose_name="Adresse email")
    nom = models.CharField(max_length=150, verbose_name="Nom")
    prenom = models.CharField(max_length=150, verbose_name="Prénom")
    role = models.CharField(
        max_length=10,
        choices=Role.choices,
        default=Role.AGENT,
        verbose_name="Rôle",
    )
    is_active = models.BooleanField(default=True, verbose_name="Actif")
    is_staff = models.BooleanField(default=False, verbose_name="Accès admin")
    date_creation = models.DateTimeField(auto_now_add=True, verbose_name="Date de création")

    objects = UtilisateurManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["nom", "prenom"]

    class Meta:
        app_label = "accounts"
        verbose_name = "Utilisateur"
        verbose_name_plural = "Utilisateurs"
        ordering = ["nom", "prenom"]

    def __str__(self):
        return f"{self.prenom} {self.nom} ({self.get_role_display()})"

    def est_admin(self):
        return self.role == self.Role.ADMIN

    def est_agent(self):
        return self.role == self.Role.AGENT