"""
Modèle CategorieOperation.

Permet de classifier les recettes et dépenses par nature comptable
(ex : Ventes, Achats, Salaires, Loyer...).
Centralisé dans core car utilisé par revenues ET expenses.
"""
from django.db import models


class CategorieOperation(models.Model):
    """
    Catégorie comptable d'une opération financière.

    Logique métier : le champ `sens` garantit qu'une catégorie de type
    RECETTE ne peut pas être assignée à une dépense, et vice-versa.
    Cette contrainte est appliquée au niveau du formulaire.
    """

    class Sens(models.TextChoices):
        RECETTE = "RECETTE", "Recette"
        DEPENSE = "DEPENSE", "Dépense"

    libelle = models.CharField(
        max_length=100,
        unique=True,
        verbose_name="Libellé",
    )
    sens = models.CharField(
        max_length=8,
        choices=Sens.choices,
        verbose_name="Sens",
    )

    class Meta:
        app_label = "core"
        verbose_name = "Catégorie d'opération"
        verbose_name_plural = "Catégories d'opérations"
        ordering = ["sens", "libelle"]

    def __str__(self):
        return f"{self.libelle} ({self.get_sens_display()})"