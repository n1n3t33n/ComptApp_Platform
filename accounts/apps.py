from django.apps import AppConfig


class AccountsConfig(AppConfig):
    """Configuration de l'application accounts : Utilisateurs et authentification."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "accounts"
    verbose_name = "Utilisateurs et authentification"