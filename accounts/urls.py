"""Routes de l'application accounts."""
from django.urls import path
from accounts.views import ConnexionView, VerificationOtpView, DeconnexionView

app_name = "accounts"

urlpatterns = [
    path("connexion/", ConnexionView.as_view(), name="connexion"),
    path("verification-otp/", VerificationOtpView.as_view(), name="verification_otp"),
    path("deconnexion/", DeconnexionView.as_view(), name="deconnexion"),
]