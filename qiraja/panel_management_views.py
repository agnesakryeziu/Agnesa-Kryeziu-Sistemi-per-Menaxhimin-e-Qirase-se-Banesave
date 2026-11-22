from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    UserPassesTestMixin,
)
from django.contrib.messages.views import SuccessMessageMixin
from django.db import transaction
from django.db.models import Q
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView

from .models import Banesa, Pronari, Qiramarresi, FotoBanese
from .panel_forms import BanesaForm, PronariForm, QiramarresiForm


class QasjaAdministratorit(LoginRequiredMixin, UserPassesTestMixin):
    login_url = reverse_lazy("hyrja")

    def test_func(self):
        return self.request.user.is_staff


class ListaAdministrimit(QasjaAdministratorit, ListView):
    template_name = "qiraja/panel_lista.html"
    context_object_name = "regjistrimet"
    paginate_by = 8

    titulli = ""
    pershkrimi = ""
    seksioni = ""
    emri_url_shto = ""
    kerko_ne = ()
    lidhjet = ()

    def get_queryset(self):
        queryset = super().get_queryset()

        if self.lidhjet:
            queryset = queryset.select_related(*self.lidhjet)

        kerkimi = self.request.GET.get("q", "").strip()

        if kerkimi:
            kushti = Q()

            for fusha in self.kerko_ne:
                kushti |= Q(**{f"{fusha}__icontains": kerkimi})

            queryset = queryset.filter(kushti)

        return queryset.order_by("-id")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["titulli"] = self.titulli
        context["pershkrimi"] = self.pershkrimi
        context["seksioni"] = self.seksioni
        context["kerkimi"] = self.request.GET.get("q", "").strip()
        context["url_shto"] = reverse(self.emri_url_shto)
        context["gjithsej"] = self.model.objects.count()

        return context


class ListaBanesave(ListaAdministrimit):
    model = Banesa
    titulli = "Menaxhimi i banesave"
    pershkrimi = "Shtoni dhe përditësoni banesat e regjistruara."
    seksioni = "banesat"
    emri_url_shto = "panel_shto_banese"
    kerko_ne = ("adresa", "qyteti")
    lidhjet = ("pronari",)


class ListaPronareve(ListaAdministrimit):
    model = Pronari
    titulli = "Menaxhimi i pronarëve"
    pershkrimi = "Menaxhoni të dhënat e pronarëve të banesave."
    seksioni = "pronaret"
    emri_url_shto = "panel_shto_pronar"
    kerko_ne = ("emri", "mbiemri", "email", "telefoni")


class ListaQiramarresve(ListaAdministrimit):
    model = Qiramarresi
    titulli = "Menaxhimi i qiramarrësve"
    pershkrimi = "Menaxhoni qiramarrësit e regjistruar."
    seksioni = "qiramarresit"
    emri_url_shto = "panel_shto_qiramarres"
    kerko_ne = ("emri", "mbiemri", "email", "telefoni")


class FormularAdministrimi(QasjaAdministratorit, SuccessMessageMixin):
    template_name = "qiraja/panel_form.html"

    titulli = ""
    pershkrimi = ""
    seksioni = ""
    emri_url_kthim = ""

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["titulli"] = self.titulli
        context["pershkrimi"] = self.pershkrimi
        context["seksioni"] = self.seksioni
        context["url_kthim"] = reverse(self.emri_url_kthim)
        context["eshte_ndryshim"] = bool(
            self.object and self.object.pk
        )

        return context


class RuajtjaFotoveBanese:
    @transaction.atomic
    def form_valid(self, form):
        fotot = form.cleaned_data.get("fotot_shtese") or []

        banesa_ekzistuese = getattr(self, "object", None)

        numri_ekzistues = 0

        if banesa_ekzistuese is not None and banesa_ekzistuese.pk:
            numri_ekzistues = (
                banesa_ekzistuese.fotot_shtese.count()
            )

        if numri_ekzistues + len(fotot) > 7:
            hapesira = max(7 - numri_ekzistues, 0)

            form.add_error(
                "fotot_shtese",
                f"Mund të shtoni edhe {hapesira} fotografi shtesë."
            )

            return self.form_invalid(form)

        response = super().form_valid(form)

        for foto in fotot:
            FotoBanese.objects.create(
                banesa=self.object,
                fotografia=foto
            )

        return response


class ShtoBanese(
    RuajtjaFotoveBanese,
    FormularAdministrimi,
    CreateView
):
    model = Banesa
    form_class = BanesaForm
    titulli = "Shto banesë"
    pershkrimi = "Regjistroni një banesë të re në sistem."
    seksioni = "banesat"
    emri_url_kthim = "panel_banesat"
    success_url = reverse_lazy("panel_banesat")
    success_message = "Banesa u shtua me sukses."


class NdryshoBanese(
    RuajtjaFotoveBanese,
    FormularAdministrimi,
    UpdateView
):
    model = Banesa
    form_class = BanesaForm
    titulli = "Përditëso banesën"
    pershkrimi = "Ndryshoni të dhënat e banesës."
    seksioni = "banesat"
    emri_url_kthim = "panel_banesat"
    success_url = reverse_lazy("panel_banesat")
    success_message = "Banesa u përditësua me sukses."


class ShtoPronar(FormularAdministrimi, CreateView):
    model = Pronari
    form_class = PronariForm
    titulli = "Shto pronar"
    pershkrimi = "Regjistroni një pronar të ri."
    seksioni = "pronaret"
    emri_url_kthim = "panel_pronaret"
    success_url = reverse_lazy("panel_pronaret")
    success_message = "Pronari u shtua me sukses."


class NdryshoPronar(FormularAdministrimi, UpdateView):
    model = Pronari
    form_class = PronariForm
    titulli = "Përditëso pronarin"
    pershkrimi = "Ndryshoni të dhënat e pronarit."
    seksioni = "pronaret"
    emri_url_kthim = "panel_pronaret"
    success_url = reverse_lazy("panel_pronaret")
    success_message = "Pronari u përditësua me sukses."


class ShtoQiramarres(FormularAdministrimi, CreateView):
    model = Qiramarresi
    form_class = QiramarresiForm
    titulli = "Shto qiramarrës"
    pershkrimi = "Regjistroni një qiramarrës të ri."
    seksioni = "qiramarresit"
    emri_url_kthim = "panel_qiramarresit"
    success_url = reverse_lazy("panel_qiramarresit")
    success_message = "Qiramarrësi u shtua me sukses."


class NdryshoQiramarres(FormularAdministrimi, UpdateView):
    model = Qiramarresi
    form_class = QiramarresiForm
    titulli = "Përditëso qiramarrësin"
    pershkrimi = "Ndryshoni të dhënat e qiramarrësit."
    seksioni = "qiramarresit"
    emri_url_kthim = "panel_qiramarresit"
    success_url = reverse_lazy("panel_qiramarresit")
    success_message = "Qiramarrësi u përditësua me sukses."
