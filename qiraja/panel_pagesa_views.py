from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView

from .models import Pagesa
from .panel_pagesa_forms import PagesaForm
from .panel_management_views import (
    ListaAdministrimit,
    FormularAdministrimi,
)


class ListaPagesave(ListaAdministrimit):
    model = Pagesa
    template_name = "qiraja/panel_pagesat.html"

    titulli = "Menaxhimi i pagesave"
    pershkrimi = "Shikoni dhe menaxhoni pagesat e qirasë."
    seksioni = "pagesat"
    emri_url_shto = "panel_shto_pagese"

    kerko_ne = (
        "kontrata__banesa__adresa",
        "kontrata__banesa__qyteti",
        "kontrata__qiramarresi__emri",
        "kontrata__qiramarresi__mbiemri",
        "kontrata__qiramarresi__email",
    )

    lidhjet = (
        "kontrata",
        "kontrata__banesa",
        "kontrata__qiramarresi",
    )


class ShtoPagese(FormularAdministrimi, CreateView):
    model = Pagesa
    form_class = PagesaForm
    template_name = "qiraja/panel_pagesa_form.html"

    titulli = "Regjistro pagesë"
    pershkrimi = "Regjistroni një pagesë të re të qirasë."
    seksioni = "pagesat"
    emri_url_kthim = "panel_pagesat"

    success_url = reverse_lazy("panel_pagesat")
    success_message = "Pagesa u regjistrua me sukses."


class NdryshoPagese(FormularAdministrimi, UpdateView):
    model = Pagesa
    form_class = PagesaForm
    template_name = "qiraja/panel_pagesa_form.html"

    titulli = "Përditëso pagesën"
    pershkrimi = "Ndryshoni të dhënat dhe statusin e pagesës."
    seksioni = "pagesat"
    emri_url_kthim = "panel_pagesat"

    success_url = reverse_lazy("panel_pagesat")
    success_message = "Pagesa u përditësua me sukses."