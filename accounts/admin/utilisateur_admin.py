"""Configuration de l'admin Django pour le modèle Utilisateur."""
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from accounts.models import Utilisateur


@admin.register(Utilisateur)
class UtilisateurAdmin(UserAdmin):
    """
    Interface admin pour la création et la gestion des comptes.
    C'est ici (et uniquement ici) que les comptes ADMIN et AGENT sont créés.
    """

    list_display = ["email", "nom", "prenom", "role", "is_active", "date_creation"]
    list_filter = ["role", "is_active"]
    search_fields = ["email", "nom", "prenom"]
    ordering = ["nom"]

    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Informations personnelles", {"fields": ("nom", "prenom")}),
        ("Rôle et accès", {"fields": ("role", "is_active", "is_staff", "is_superuser")}),
        ("Permissions", {"fields": ("groups", "user_permissions")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "nom", "prenom", "role", "password1", "password2"),
            },
        ),
    )