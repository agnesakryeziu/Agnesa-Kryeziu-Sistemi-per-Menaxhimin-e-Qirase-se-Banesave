from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import ListView, View

from .models import MesazhKontakti, Abonenti


class QasjaAdministratoritMixin(LoginRequiredMixin):

    login_url = "hyrja"

    def dispatch(self, request, *args, **kwargs):

        if not request.user.is_authenticated:
            return self.handle_no_permission()

        if not request.user.is_staff:
            raise PermissionDenied

        return super().dispatch(request, *args, **kwargs)


class ListaMesazheve(QasjaAdministratoritMixin, ListView):

    model = MesazhKontakti
    template_name = "qiraja/panel_komunikimi.html"
    context_object_name = "mesazhet"

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        context["seksioni"] = "mesazhet"
        context["titulli"] = "Mesazhet e kontaktit"
        context["gjithsej"] = MesazhKontakti.objects.count()
        context["palexuara"] = MesazhKontakti.objects.filter(
            i_lexuar=False
        ).count()

        context["lexuara"] = MesazhKontakti.objects.filter(
            i_lexuar=True
        ).count()

        return context


class LexoMesazhin(QasjaAdministratoritMixin, View):

    http_method_names = ["post"]

    def post(self, request, pk):

        mesazhi = get_object_or_404(
            MesazhKontakti,
            pk=pk
        )

        mesazhi.i_lexuar = True
        mesazhi.save(update_fields=["i_lexuar"])

        messages.success(
            request,
            "Mesazhi u shënua si i lexuar."
        )

        return redirect("panel_mesazhet")


class ListaAbonenteve(QasjaAdministratoritMixin, ListView):

    model = Abonenti
    template_name = "qiraja/panel_komunikimi.html"
    context_object_name = "abonentet"

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        context["seksioni"] = "abonentet"
        context["titulli"] = "Abonentët"
        context["gjithsej"] = Abonenti.objects.count()

        context["aktive"] = Abonenti.objects.filter(
            aktiv=True
        ).count()

        context["joaktive"] = Abonenti.objects.filter(
            aktiv=False
        ).count()

        return context


class NdryshoStatusinAbonentit(QasjaAdministratoritMixin, View):

    http_method_names = ["post"]

    def post(self, request, pk):

        abonenti = get_object_or_404(
            Abonenti,
            pk=pk
        )

        abonenti.aktiv = not abonenti.aktiv
        abonenti.save(update_fields=["aktiv"])

        messages.success(
            request,
            "Statusi i abonentit u përditësua."
        )

        return redirect("panel_abonentet")