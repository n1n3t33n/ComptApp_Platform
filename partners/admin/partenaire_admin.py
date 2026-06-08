"""Configuration de l'admin Django pour le modèle Partenaire."""
from django.contrib import admin

from partners.models import Partenaire


@admin.register(Partenaire)
class PartenaireAdmin(admin.ModelAdmin):
    list_display = ["nom", "type", "telephone", "email", "date_creation"]
    list_filter = ["type"]
    search_fields = ["nom", "email"]