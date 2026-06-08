from django.apps import AppConfig


class ExpensesConfig(AppConfig):
    """Configuration de l'application expenses : Dépenses."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "expenses"
    verbose_name = "Dépenses"