from django.apps import AppConfig


class ReportsConfig(AppConfig):
    """Configuration de l'application reports : Rapports comptables."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "reports"
    verbose_name = "Rapports comptables"