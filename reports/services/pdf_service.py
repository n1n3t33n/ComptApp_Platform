"""
Service de génération PDF.

Convertit un gabarit HTML rendu en document PDF grâce à WeasyPrint.
Réutilise les templates Django : le même HTML sert à l'affichage écran
et au PDF, ce qui garantit la cohérence visuelle.
"""
from django.http import HttpResponse
from django.template.loader import render_to_string
from weasyprint import HTML


def generer_pdf(template_name, context, nom_fichier):
    """
    Rend un template HTML avec son contexte et retourne une réponse HTTP
    contenant le PDF généré (téléchargement déclenché côté navigateur).
    """
    html_rendu = render_to_string(template_name, context)
    pdf = HTML(string=html_rendu).write_pdf()

    reponse = HttpResponse(pdf, content_type="application/pdf")
    reponse["Content-Disposition"] = f'attachment; filename="{nom_fichier}"'
    return reponse