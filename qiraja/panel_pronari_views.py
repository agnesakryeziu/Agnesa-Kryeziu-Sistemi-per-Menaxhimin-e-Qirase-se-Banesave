from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.views.generic import TemplateView
from django.utils import timezone

from .models import Pronari, Banesa, Kontrata, Pagesa


class PaneliPronarit(LoginRequiredMixin, TemplateView):
    template_name = "qiraja/panel_pronari.html"
    login_url = "hyrja"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        perdoruesi = self.request.user

        if perdoruesi.is_staff or perdoruesi.roli != "pronar":
            raise PermissionDenied(
                "Kjo faqe është vetëm për pronarët."
            )

        pronari = Pronari.objects.filter(
            perdoruesi=perdoruesi
        ).first()

        if pronari is None:
            raise PermissionDenied(
                "Profili i pronarit nuk ekziston."
            )

        banesat = Banesa.objects.filter(
            pronari=pronari
        ).order_by("-id")

        kontratat = Kontrata.objects.filter(
            banesa__pronari=pronari
        )

        sot = timezone.localdate()

        kontratat_aktive = kontratat.filter(
            status="aktive",
            data_fillimit__lte=sot,
            data_mbarimit__gte=sot
        )

        pagesat = Pagesa.objects.filter(
            kontrata__banesa__pronari=pronari
        )

        context.update({
            "pronari": pronari,
            "banesat": banesat,
            "numri_banesave": banesat.count(),
            "numri_kontratave": kontratat_aktive.count(),
            "numri_pagesave": pagesat.count(),
            "pagesat_e_paguara": pagesat.filter(
                e_paguar=True
            ).count(),
        })

        return context