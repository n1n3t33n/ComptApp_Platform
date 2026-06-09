"""
Service de génération PDF.

Convertit un gabarit HTML rendu en document PDF grâce à xhtml2pdf (pisa),
qui s'installe en pur pip sans dépendance système (contrairement à WeasyPrint
qui nécessite GTK sous Windows).

L'import est différé pour que l'absence de la librairie n'empêche pas
le reste de l'application de fonctionner.
"""
from django.http import HttpResponse
from django.template.loader import render_to_string


def generer_pdf(template_name, context, nom_fichier):
    """
    Rend un template HTML avec son contexte et retourne une réponse HTTP
    contenant le PDF généré (téléchargement déclenché côté navigateur).

    Les templates destinés au PDF doivent utiliser des tables pour la mise
    en page (pas de flexbox ni grid — non supportés par xhtml2pdf).
    """
    try:
        from xhtml2pdf import pisa
    except ImportError:
        return HttpResponse(
            "La génération PDF n'est pas disponible : la librairie xhtml2pdf "
            "n'est pas installée. Lancez : pip install xhtml2pdf",
            content_type="text/plain; charset=utf-8",
            status=503,
        )

    html_rendu = render_to_string(template_name, context)

    reponse = HttpResponse(content_type="application/pdf")
    reponse["Content-Disposition"] = f'attachment; filename="{nom_fichier}"'

    resultat = pisa.CreatePDF(html_rendu, dest=reponse, encoding="utf-8")

    if resultat.err:
        return HttpResponse(
            "Erreur lors de la génération du PDF. Veuillez réessayer.",
            content_type="text/plain; charset=utf-8",
            status=500,
        )

    return reponse
