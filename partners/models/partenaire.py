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
    activite = models.CharField(
        max_length=120,
        blank=True,
        verbose_name="Secteur d'activité",
        help_text="Ex. : Commerce de détail, BTP, Restauration, Transport…",
    )
    contact = models.CharField(
        max_length=150,
        blank=True,
        verbose_name="Personne à contacter",
    )
    telephone = models.CharField(max_length=20, blank=True, verbose_name="Téléphone")
    email = models.EmailField(blank=True, verbose_name="Email")
    ville = models.CharField(max_length=100, blank=True, verbose_name="Ville")
    adresse = models.TextField(blank=True, verbose_name="Adresse")
    notes = models.TextField(blank=True, verbose_name="Notes internes")
    date_creation = models.DateTimeField(auto_now_add=True)

    class Meta:
        app_label = "partners"
        verbose_name = "Partenaire"
        verbose_name_plural = "Partenaires"
        ordering = ["type", "nom"]

    def __str__(self):
        return f"{self.nom} ({self.get_type_display()})"