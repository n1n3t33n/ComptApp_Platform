"""Configuration de l'admin Django pour le modèle Depense."""
from django.contrib import admin

from expenses.models import Depense


@admin.register(Depense)
class DepenseAdmin(admin.ModelAdmin):
    list_display = ["date", "montant", "categorie", "partenaire", "saisi_par"]
    list_filter = ["categorie", "date"]
    search_fields = ["description"]
    date_hierarchy = "date"