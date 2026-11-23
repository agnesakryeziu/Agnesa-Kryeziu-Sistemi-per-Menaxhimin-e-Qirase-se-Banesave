from django.contrib import messages
from django.db import transaction
from django.db.models.deletion import ProtectedError
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import DeleteView

from .models import Banesa, Pronari, Qiramarresi, Kontrata
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


class FshiPerson(QasjaAdministratorit, DeleteView):
    template_name = "qiraja/panel_konfirmo_fshirjen.html"
    context_object_name = "personi"

    lloji = ""
    emri_url_kthim = ""
    mesazhi_suksesit = ""

    def ka_te_dhena_te_lidhura(self, personi):
        return False

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["titulli"] = "Fshi " + self.lloji
        context["lloji"] = self.lloji
        context["url_kthim"] = self.success_url
        context["ka_lidhje"] = self.ka_te_dhena_te_lidhura(
            self.object
        )

        return context

    def form_valid(self, form):
        personi = self.object

        if self.ka_te_dhena_te_lidhura(personi):
            messages.error(
                self.request,
                "Ky regjistrim nuk mund të fshihet sepse "
                "ka të dhëna të lidhura me të."
            )

            return redirect(self.emri_url_kthim)

        try:
            with transaction.atomic():
                response = super().form_valid(form)

        except ProtectedError:
            messages.error(
                self.request,
                "Regjistrimi nuk mund të fshihet sepse "
                "përdoret në të dhëna të tjera."
            )

            return redirect(self.emri_url_kthim)

        messages.success(
            self.request,
            self.mesazhi_suksesit
        )

        return response


class FshiPronar(FshiPerson):
    model = Pronari
    lloji = "pronarin"
    emri_url_kthim = "panel_pronaret"
    success_url = reverse_lazy("panel_pronaret")
    mesazhi_suksesit = "Pronari u fshi me sukses."

    def ka_te_dhena_te_lidhura(self, personi):
        return Banesa.objects.filter(
            pronari=personi
        ).exists()


class FshiQiramarres(FshiPerson):
    model = Qiramarresi
    lloji = "qiramarrësin"
    emri_url_kthim = "panel_qiramarresit"
    success_url = reverse_lazy("panel_qiramarresit")
    mesazhi_suksesit = "Qiramarrësi u fshi me sukses."

    def ka_te_dhena_te_lidhura(self, personi):
        return Kontrata.objects.filter(
            qiramarresi=personi
        ).exists()