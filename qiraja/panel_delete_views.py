from django.contrib import messages
from django.db import transaction
from django.db.models.deletion import ProtectedError
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import DeleteView

from .models import Banesa
from .panel_management_views import QasjaAdministratorit


class FshiBanese(QasjaAdministratorit, DeleteView):
    model = Banesa
    template_name = "qiraja/panel_konfirmo_fshirjen.html"
    context_object_name = "banesa"
    success_url = reverse_lazy("panel_banesat")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["titulli"] = "Fshi banesën"
        context["pershkrimi"] = (
            "Konfirmoni fshirjen e banesës nga sistemi."
        )
        context["seksioni"] = "banesat"
        return context

    def form_valid(self, form):
        banesa = self.object

        if banesa.kontratat.exists():
            messages.error(
                self.request,
                "Kjo banesë nuk mund të fshihet sepse ka "
                "kontrata të regjistruara."
            )
            return redirect("panel_banesat")

        skedaret = []

        if banesa.fotografia:
            skedaret.append(
                (
                    banesa.fotografia.storage,
                    banesa.fotografia.name,
                )
            )

        for foto in banesa.fotografite.all():
            if foto.fotografia:
                skedaret.append(
                    (
                        foto.fotografia.storage,
                        foto.fotografia.name,
                    )
                )

        for foto in banesa.fotot_shtese.all():
            if foto.fotografia:
                skedaret.append(
                    (
                        foto.fotografia.storage,
                        foto.fotografia.name,
                    )
                )

        try:
            with transaction.atomic():
                response = super().form_valid(form)

                def pastro_skedaret():
                    for storage, emri in skedaret:
                        if emri:
                            storage.delete(emri)

                transaction.on_commit(
                    pastro_skedaret,
                    robust=True,
                )

        except ProtectedError:
            messages.error(
                self.request,
                "Banesa nuk mund të fshihet sepse "
                "ka të dhëna të lidhura."
            )
            return redirect("panel_banesat")

        messages.success(
            self.request,
            "Banesa u fshi me sukses."
        )

        return response