"""Package admin de l'application core."""
from django.contrib import admin
from core.models import CategorieOperation


@admin.register(CategorieOperation)
class CategorieOperationAdmin(admin.ModelAdmin):
    list_display = ["libelle", "sens"]
    list_filter = ["sens"]
    search_fields = ["libelle"]