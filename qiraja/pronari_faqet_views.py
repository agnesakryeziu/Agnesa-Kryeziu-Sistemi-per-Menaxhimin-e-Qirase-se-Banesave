from django.views.generic import ListView, TemplateView

from .models import Banesa, Kontrata, Pagesa
from .pronari_banesat_views import QasjaPronaritMixin


class BanesatPronarit(QasjaPronaritMixin, ListView):

    model = Banesa
    template_name = "qiraja/pronari_faqet.html"
    context_object_name = "banesat"
    extra_context = {
        "seksioni": "banesat",
        "titulli": "Banesat e mia",
        "pershkrimi": "Menaxhoni banesat tuaja personale."
    }

    def get_queryset(self):
        return Banesa.objects.filter(
            pronari=self.pronari
        ).order_by("-id")


class KontratatPronarit(QasjaPronaritMixin, ListView):

    model = Kontrata
    template_name = "qiraja/pronari_faqet.html"
    context_object_name = "kontratat"
    extra_context = {
        "seksioni": "kontratat",
        "titulli": "Kontratat e mia",
        "pershkrimi": "Shikoni kontratat e banesave tuaja."
    }

    def get_queryset(self):
        return Kontrata.objects.filter(
            banesa__pronari=self.pronari
        ).select_related(
            "banesa", "qiramarresi"
        ).order_by("-data_fillimit")


class PagesatPronarit(QasjaPronaritMixin, ListView):

    model = Pagesa
    template_name = "qiraja/pronari_faqet.html"
    context_object_name = "pagesat"
    extra_context = {
        "seksioni": "pagesat",
        "titulli": "Pagesat e mia",
        "pershkrimi": "Shikoni pagesat e qirasë së banesave tuaja."
    }

    def get_queryset(self):
        return Pagesa.objects.filter(
            kontrata__banesa__pronari=self.pronari
        ).select_related(
            "kontrata__banesa",
            "kontrata__qiramarresi"
        ).order_by("-data_pageses")


class ProfiliPronarit(QasjaPronaritMixin, TemplateView):

    template_name = "qiraja/pronari_faqet.html"
    extra_context = {
        "seksioni": "profili",
        "titulli": "Profili im",
        "pershkrimi": "Informacionet e llogarisë suaj personale."
    }