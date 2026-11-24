from django.contrib import messages
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils import timezone
from django.views import View

from .models import Kontrata
from .panel_management_views import QasjaAdministratorit


class AnuloKontrate(QasjaAdministratorit, View):
    template_name = "qiraja/panel_konfirmo_fshirjen.html"

    def get(self, request, pk):
        kontrata = get_object_or_404(
            Kontrata.objects.select_related(
                "banesa",
                "qiramarresi"
            ),
            pk=pk
        )

        if kontrata.status == "anuluar":
            messages.info(
                request,
                "Kjo kontratë është anuluar më parë."
            )
            return redirect("panel_kontratat")

        if kontrata.data_mbarimit < timezone.localdate():
            messages.warning(
                request,
                "Kjo kontratë ka përfunduar dhe nuk mund të anulohet."
            )
            return redirect("panel_kontratat")

        return render(
            request,
            self.template_name,
            {
                "titulli": "Anulo kontratën",
                "kontrata": kontrata,
                "seksioni": "kontratat",
                "url_kthim": reverse("panel_kontratat"),
            }
        )

    def post(self, request, pk):
        with transaction.atomic():
            kontrata = get_object_or_404(
                Kontrata.objects.select_for_update(),
                pk=pk
            )

            if kontrata.status == "anuluar":
                messages.info(
                    request,
                    "Kjo kontratë është anuluar më parë."
                )
                return redirect("panel_kontratat")

            if kontrata.data_mbarimit < timezone.localdate():
                messages.warning(
                    request,
                    "Kjo kontratë ka përfunduar dhe nuk mund të anulohet."
                )
                return redirect("panel_kontratat")

            kontrata.status = "anuluar"
            kontrata.data_anulimit = timezone.localdate()

            kontrata.save(
                update_fields=[
                    "status",
                    "data_anulimit"
                ]
            )

        messages.success(
            request,
            "Kontrata u anulua me sukses."
        )

        return redirect("panel_kontratat")
