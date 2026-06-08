"""Configuration de l'admin Django pour le modèle Recette."""
from django.contrib import admin

from revenues.models import Recette


@admin.register(Recette)
class RecetteAdmin(admin.ModelAdmin):
    list_display = ["date", "montant", "categorie", "partenaire", "saisi_par"]
    list_filter = ["categorie", "date"]
    search_fields = ["description"]
    date_hierarchy = "date"