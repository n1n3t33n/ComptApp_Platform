"""
Utilitaires partagés de l'application core.

Fournit des décorateurs et mixins pour le contrôle d'accès basé sur les rôles.
"""
from functools import wraps

from django.contrib import messages
from django.shortcuts import redirect


def admin_requis(view_func):
    """
    Décorateur réservant une vue aux utilisateurs avec le rôle ADMIN.
    Redirige vers le tableau de bord avec un message d'erreur si accès refusé.
    À placer après @login_required (ou équivalent) pour éviter une double vérification.
    """
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect("accounts:connexion")
        if not request.user.est_admin():
            messages.error(request, "Accès réservé aux administrateurs.")
            return redirect("core:tableau_de_bord")
        return view_func(request, *args, **kwargs)
    return wrapper


class AdminRequisMixin:
    """
    Mixin CBV équivalent de @admin_requis pour les vues basées sur des classes.
    Utiliser avec @method_decorator(login_required, name='dispatch') en plus.
    """
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect("accounts:connexion")
        if not request.user.est_admin():
            messages.error(request, "Accès réservé aux administrateurs.")
            return redirect("core:tableau_de_bord")
        return super().dispatch(request, *args, **kwargs)
