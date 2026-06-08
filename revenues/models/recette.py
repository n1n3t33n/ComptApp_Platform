"""
Modèle Recette.

Logique métier : une recette est une entrée d'argent dans la trésorerie.
Elle est obligatoirement classée dans une CategorieOperation de sens RECETTE.
Le lien vers un Partenaire (client) est facultatif mais recommandé pour le
suivi comptable. La date de saisie est automatique pour la traçabilité.
"""
from django.conf import settings
from django.db import models

from core.models import CategorieOperation
from partners.models import Partenaire


class Recette(models.Model):

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
        limit_choices_to={"type": Partenaire.Type.CLIENT},
        related_name="recettes",
        verbose_name="Client",
    )
    categorie = models.ForeignKey(
        CategorieOperation,
        on_delete=models.PROTECT,
        limit_choices_to={"sens": CategorieOperation.Sens.RECETTE},
        related_name="recettes",
        verbose_name="Catégorie",
    )
    saisi_par = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="recettes_saisies",
        verbose_name="Saisi par",
    )
    date_saisie = models.DateTimeField(auto_now_add=True, verbose_name="Date de saisie")

    class Meta:
        app_label = "revenues"
        verbose_name = "Recette"
        verbose_name_plural = "Recettes"
        ordering = ["-date", "-date_saisie"]

    def __str__(self):
        return f"Recette {self.date} — {self.montant} FCFA — {self.categorie}"