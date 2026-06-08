from django.apps import AppConfig


class CoreConfig(AppConfig):
    """Configuration de l'application core : Noyau et tableau de bord."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "core"
    verbose_name = "Noyau et tableau de bord"