"""
Modèle Depense.

Logique métier : une dépense est une sortie d'argent de la trésorerie.
Structure miroir de Recette, avec le lien Partenaire filtré sur FOURNISSEUR
et la catégorie de sens DEPENSE.
"""
from django.conf import settings
from django.db import models

from core.models import CategorieOperation
from partners.models import Partenaire


class Depense(models.Model):

    date = models.DateField(verbose_name="Date de l'opération")
    montant = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        verbose_name="Montant (FCFA)",
    )
    description = models.TextField(verbose_name="Description / Libellé")
    partenaire = models.ForeignKey(
        Partenaire,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        limit_choices_to={"type": Partenaire.Type.FOURNISSEUR},
        related_name="depenses",
        verbose_name="Fournisseur",
    )
    categorie = models.ForeignKey(
        CategorieOperation,
        on_delete=models.PROTECT,
        limit_choices_to={"sens": CategorieOperation.Sens.DEPENSE},
        related_name="depenses",
        verbose_name="Catégorie",
    )
    saisi_par = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="depenses_saisies",
        verbose_name="Saisi par",
    )
    date_saisie = models.DateTimeField(auto_now_add=True, verbose_name="Date de saisie")

    class Meta:
        app_label = "expenses"
        verbose_name = "Dépense"
        verbose_name_plural = "Dépenses"
        ordering = ["-date", "-date_saisie"]

    def __str__(self):
        return f"Dépense {self.date} — {self.montant} FCFA — {self.categorie}"