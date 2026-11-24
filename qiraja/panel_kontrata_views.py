from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView

from .models import Kontrata
from .panel_kontrata_forms import KontrataForm
from .panel_management_views import (
    ListaAdministrimit,
    FormularAdministrimi,
)


class ListaKontratave(ListaAdministrimit):
    model = Kontrata
    template_name = "qiraja/panel_kontratat.html"

    titulli = "Menaxhimi i kontratave"
    pershkrimi = "Menaxhoni kontratat e qirasë së banesave."
    seksioni = "kontratat"
    emri_url_shto = "panel_shto_kontrate"

    kerko_ne = (
        "banesa__adresa",
        "banesa__qyteti",
        "qiramarresi__emri",
        "qiramarresi__mbiemri",
        "qiramarresi__email",
    )

    lidhjet = (
        "banesa",
        "qiramarresi",
    )


class ShtoKontrate(FormularAdministrimi, CreateView):
    model = Kontrata
    form_class = KontrataForm
    template_name = "qiraja/panel_kontrata_form.html"

    titulli = "Shto kontratë"
    pershkrimi = "Regjistroni një kontratë të re të qirasë."
    seksioni = "kontratat"
    emri_url_kthim = "panel_kontratat"

    success_url = reverse_lazy("panel_kontratat")
    success_message = "Kontrata u shtua me sukses."


class NdryshoKontrate(FormularAdministrimi, UpdateView):
    model = Kontrata
    form_class = KontrataForm
    template_name = "qiraja/panel_kontrata_form.html"

    titulli = "Përditëso kontratën"
    pershkrimi = "Ndryshoni të dhënat e kontratës."
    seksioni = "kontratat"
    emri_url_kthim = "panel_kontratat"

    success_url = reverse_lazy("panel_kontratat")
    success_message = "Kontrata u përditësua me sukses."