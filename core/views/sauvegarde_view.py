"""
Vue : Sauvegarde et restauration des données (Module 6).

Réservée aux ADMIN uniquement. Permet :
- Export : génère un dump JSON de toute la base via dumpdata et le propose
  en téléchargement.
- Import : accepte un fichier JSON uploadé et le charge via loaddata (les
  données existantes sont conservées ; loaddata insère ou met à jour).
"""
import io
import os
import tempfile

from django.contrib import messages
from django.core.management import call_command
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.utils import timezone
from django.views import View

from core.utils import AdminRequisMixin


class SauvegardeView(AdminRequisMixin, View):
    """Page de sauvegarde / restauration, réservée aux administrateurs."""

    template_name = "core/admin/sauvegarde.html"

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        action = request.POST.get("action", "")

        if action == "exporter":
            return self._exporter(request)
        if action == "importer":
            return self._importer(request)

        messages.error(request, "Action inconnue.")
        return redirect("core:sauvegarde")

    # ------------------------------------------------------------------
    def _exporter(self, request):
        """Dump toute la base en JSON et retourne la réponse en téléchargement."""
        contenu = io.StringIO()
        try:
            call_command(
                "dumpdata",
                "--natural-foreign",
                "--natural-primary",
                "--indent", "2",
                "--exclude", "contenttypes",
                "--exclude", "auth.permission",
                stdout=contenu,
            )
        except Exception as exc:
            messages.error(request, f"Erreur lors de l'export : {exc}")
            return redirect("core:sauvegarde")

        date_str = timezone.localdate().strftime("%Y%m%d")
        reponse = HttpResponse(contenu.getvalue(), content_type="application/json")
        reponse["Content-Disposition"] = f'attachment; filename="comptapp_sauvegarde_{date_str}.json"'
        return reponse

    def _importer(self, request):
        """Charge un fichier JSON uploadé via loaddata."""
        fichier = request.FILES.get("fichier_sauvegarde")
        if not fichier:
            messages.error(request, "Aucun fichier sélectionné.")
            return redirect("core:sauvegarde")

        if not fichier.name.endswith(".json"):
            messages.error(request, "Le fichier doit être au format JSON (.json).")
            return redirect("core:sauvegarde")

        # Écriture dans un fichier temporaire (loaddata nécessite un chemin sur disque)
        with tempfile.NamedTemporaryFile(
            suffix=".json", delete=False, mode="wb"
        ) as tmp:
            for chunk in fichier.chunks():
                tmp.write(chunk)
            chemin_tmp = tmp.name

        try:
            call_command("loaddata", chemin_tmp, verbosity=0)
            messages.success(request, "Restauration effectuée avec succès.")
        except Exception as exc:
            messages.error(request, f"Erreur lors de la restauration : {exc}")
        finally:
            os.unlink(chemin_tmp)

        return redirect("core:sauvegarde")
