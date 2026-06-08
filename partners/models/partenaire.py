"""
Modèle Partenaire (Client ou Fournisseur).

Logique métier : Client et Fournisseur partagent exactement la même
structure de données. On les unifie avec un champ `type` pour éviter
la duplication et permettre qu'une même entité soit à la fois client
et fournisseur (cas fréquent en comptabilité).
"""
from django.db import models


class Partenaire(models.Model):

    class Type(models.TextChoices):
        CLIENT = "CLIENT", "Client"
        FOURNISSEUR = "FOURNISSEUR", "Fournisseur"

    type = models.CharField(
        max_length=11,
        choices=Type.choices,
        verbose_name="Type",
    )
    nom = models.CharField(max_length=150, verbose_name="Nom ou raison sociale")
    telephone = models.CharField(max_length=20, blank=True, verbose_name="Téléphone")
    adresse = models.TextField(blank=True, verbose_name="Adresse")
    email = models.EmailField(blank=True, verbose_name="Email")
    date_creation = models.DateTimeField(auto_now_add=True)

    class Meta:
        app_label = "partners"
        verbose_name = "Partenaire"
        verbose_name_plural = "Partenaires"
        ordering = ["type", "nom"]

    def __str__(self):
        return f"{self.nom} ({self.get_type_display()})"