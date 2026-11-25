from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.views.generic import ListView

from .models import Rezervimi


class RezervimetKlientit(LoginRequiredMixin, ListView):

    login_url = "hyrja"
    template_name = "qiraja/rezervimet_pasqyra.html"
    context_object_name = "rezervimet"
    extra_context = {
        "titulli": "Rezervimet e mia",
        "administratori": False
    }

    def get_queryset(self):

        user = self.request.user

        if user.is_staff or user.roli != "klient":
            raise PermissionDenied

        return Rezervimi.objects.filter(
            klienti=user
        ).select_related("banesa")


class RezervimetAdministratorit(LoginRequiredMixin, ListView):

    login_url = "hyrja"
    template_name = "qiraja/rezervimet_pasqyra.html"
    context_object_name = "rezervimet"
    extra_context = {
        "titulli": "Të gjitha rezervimet",
        "administratori": True
    }

    def get_queryset(self):

        if not self.request.user.is_staff:
            raise PermissionDenied

        return Rezervimi.objects.select_related(
            "banesa__pronari", "klienti"
        ).all()