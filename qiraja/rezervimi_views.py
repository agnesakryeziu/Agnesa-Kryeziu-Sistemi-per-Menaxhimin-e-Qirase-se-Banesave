from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.db import transaction
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import FormView

from .models import Banesa, Rezervimi, Kontrata
from .rezervimi_forms import RezervimiForm


class RezervoBanese(LoginRequiredMixin, FormView):

    login_url = "hyrja"
    template_name = "qiraja/rezervo_banese.html"
    form_class = RezervimiForm
    success_url = reverse_lazy("klienti_rezervimet")

    def dispatch(self, request, *args, **kwargs):

        if not request.user.is_authenticated:
            return self.handle_no_permission()

        if request.user.is_staff or request.user.roli != "klient":
            raise PermissionDenied(
                "Vetëm klientët mund të rezervojnë banesa."
            )

        self.banesa = get_object_or_404(
            Banesa,
            pk=kwargs["pk"]
        )

        return super().dispatch(
            request, *args, **kwargs
        )

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        context["banesa"] = self.banesa

        return context

    @transaction.atomic
    def form_valid(self, form):

        banesa = get_object_or_404(
            Banesa.objects.select_for_update(),
            pk=self.banesa.pk
        )

        klienti = self.request.user
        sot = timezone.localdate()

        if Rezervimi.objects.filter(
            banesa=banesa,
            klienti=klienti
        ).exists():

            form.add_error(
                None,
                "Ju keni dërguar tashmë një kërkesë për këtë banesë."
            )

            return self.form_invalid(form)

        if Kontrata.objects.filter(
            banesa=banesa,
            status="aktive",
            data_fillimit__lte=sot,
            data_mbarimit__gte=sot
        ).exists():

            form.add_error(
                None,
                "Kjo banesë aktualisht është e zënë."
            )

            return self.form_invalid(form)

        if Rezervimi.objects.filter(
            banesa=banesa,
            statusi="pranuar"
        ).exists():

            form.add_error(
                None,
                "Kjo banesë ka një rezervim të pranuar."
            )

            return self.form_invalid(form)

        Rezervimi.objects.create(
            banesa=banesa,
            klienti=klienti,
            mesazhi=form.cleaned_data["mesazhi"],
            statusi="ne_pritje"
        )

        messages.success(
            self.request,
            "Kërkesa për rezervim u dërgua me sukses."
        )

        return super().form_valid(form)