from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView

from .models import Banesa, Pronari
from .pronari_forms import BanesaPronaritForm


class QasjaPronaritMixin(LoginRequiredMixin):

    login_url = "hyrja"

    def dispatch(self, request, *args, **kwargs):

        if not request.user.is_authenticated:
            return self.handle_no_permission()

        if request.user.is_staff or request.user.roli != "pronar":
            raise PermissionDenied(
                "Kjo faqe është vetëm për pronarët."
            )

        self.pronari = Pronari.objects.filter(
            perdoruesi=request.user
        ).first()

        if self.pronari is None:
            raise PermissionDenied(
                "Profili i pronarit nuk ekziston."
            )

        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["pronari"] = self.pronari
        return context


class ShtoBanesePronari(QasjaPronaritMixin, CreateView):

    model = Banesa
    form_class = BanesaPronaritForm
    template_name = "qiraja/pronari_banesa_form.html"
    success_url = reverse_lazy("paneli_pronarit")

    def form_valid(self, form):

        form.instance.pronari = self.pronari

        response = super().form_valid(form)

        messages.success(
            self.request,
            "Banesa u regjistrua me sukses."
        )

        return response

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        context["titulli"] = "Shto banesë"

        context["pershkrimi"] = (
            "Regjistroni një banesë të re në llogarinë tuaj."
        )

        context["butoni"] = "Regjistro banesën"

        return context


class NdryshoBanesePronari(QasjaPronaritMixin, UpdateView):

    model = Banesa
    form_class = BanesaPronaritForm
    template_name = "qiraja/pronari_banesa_form.html"
    success_url = reverse_lazy("paneli_pronarit")

    def get_queryset(self):

        return Banesa.objects.filter(
            pronari=self.pronari
        )

    def form_valid(self, form):

        response = super().form_valid(form)

        messages.success(
            self.request,
            "Të dhënat e banesës u përditësuan me sukses."
        )

        return response

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        context["titulli"] = "Ndrysho banesën"

        context["pershkrimi"] = (
            "Përditësoni informacionet e banesës suaj."
        )

        context["butoni"] = "Ruaj ndryshimet"

        return context