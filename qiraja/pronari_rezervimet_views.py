from django.contrib import messages
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect
from django.utils import timezone
from django.views.generic import ListView, View

from .models import Banesa, Rezervimi, Kontrata
from .pronari_banesat_views import QasjaPronaritMixin


class ListaRezervimevePronari(QasjaPronaritMixin, ListView):

    model = Rezervimi
    template_name = "qiraja/pronari_rezervimet.html"
    context_object_name = "rezervimet"

    def get_queryset(self):

        return Rezervimi.objects.filter(
            banesa__pronari=self.pronari
        ).select_related(
            "banesa", "klienti"
        ).order_by("-data_kerkese")

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        rezervimet = self.get_queryset()

        context["numri_rezervimeve"] = rezervimet.count()

        context["ne_pritje"] = rezervimet.filter(
            statusi="ne_pritje"
        ).count()

        context["pranuar"] = rezervimet.filter(
            statusi="pranuar"
        ).count()

        context["refuzuar"] = rezervimet.filter(
            statusi__in=["refuzuar", "anuluar"]
        ).count()

        return context


class VendimiRezervimit(QasjaPronaritMixin, View):

    http_method_names = ["post"]

    @transaction.atomic
    def post(self, request, pk, *args, **kwargs):

        kerkesa = get_object_or_404(
            Rezervimi,
            pk=pk,
            banesa__pronari=self.pronari
        )

        banesa = get_object_or_404(
            Banesa.objects.select_for_update(),
            pk=kerkesa.banesa_id,
            pronari=self.pronari
        )

        rezervimi = get_object_or_404(
            Rezervimi.objects.select_for_update(),
            pk=pk,
            banesa=banesa
        )

        vendimi = request.POST.get("vendimi")

        if vendimi == "anulo":

            if rezervimi.statusi != "pranuar":
                messages.error(request, "Rezervimi nuk mund te anulohet.")
                return redirect("pronari_rezervimet")

            rezervimi.statusi = "anuluar"
            rezervimi.save(update_fields=["statusi"])

            messages.success(request, "Rezervimi u anulua me sukses.")

            return redirect("pronari_rezervimet")

        if rezervimi.statusi != "ne_pritje":

            messages.error(
                request,
                "Për këtë kërkesë është marrë tashmë një vendim."
            )

            return redirect("pronari_rezervimet")

        if vendimi == "prano":

            sot = timezone.localdate()

            if Kontrata.objects.filter(
                banesa=banesa,
                status="aktive",
                data_fillimit__lte=sot,
                data_mbarimit__gte=sot
            ).exists():

                messages.error(
                    request,
                    "Kjo banesë aktualisht është e zënë."
                )

                return redirect("pronari_rezervimet")

            if Rezervimi.objects.filter(
                banesa=banesa,
                statusi="pranuar"
            ).exists():

                messages.error(
                    request,
                    "Kjo banesë ka një rezervim të pranuar."
                )

                return redirect("pronari_rezervimet")

            rezervimi.statusi = "pranuar"

            rezervimi.save(
                update_fields=["statusi"]
            )

            Rezervimi.objects.filter(
                banesa=banesa,
                statusi="ne_pritje"
            ).exclude(
                pk=rezervimi.pk
            ).update(
                statusi="refuzuar"
            )

            messages.success(
                request,
                "Rezervimi u pranua me sukses."
            )

        elif vendimi == "refuzo":

            rezervimi.statusi = "refuzuar"

            rezervimi.save(
                update_fields=["statusi"]
            )

            messages.success(
                request,
                "Rezervimi u refuzua me sukses."
            )

        else:

            messages.error(
                request,
                "Vendimi i përzgjedhur nuk është i vlefshëm."
            )

        return redirect("pronari_rezervimet")
