from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    UserPassesTestMixin,
)
from django.contrib.messages.views import SuccessMessageMixin
from django.db import transaction
from django.db.models import Q, Max
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView

from .models import (
    Banesa,
    Pronari,
    Qiramarresi,
    FotografiaBaneses,
)
from .panel_forms import (
    BanesaForm,
    PronariForm,
    QiramarresiForm,
)


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
                kushti |= Q(
                    **{f"{fusha}__icontains": kerkimi}
                )

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


class FormularAdministrimi(
    QasjaAdministratorit,
    SuccessMessageMixin
):
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
    def planifiko_fshirjen_e_skedarit(self, fusha):
        if not fusha or not fusha.name:
            return

        emri = fusha.name
        storage = fusha.storage

        transaction.on_commit(
            lambda: storage.delete(emri),
            robust=True
        )

    @transaction.atomic
    def form_valid(self, form):
        fotot_e_reja = list(
            form.cleaned_data.get("fotot_shtese") or []
        )

        fotot_per_fshirje = list(
            form.cleaned_data.get("fotot_per_fshirje") or []
        )

        hiq_foto_kryesore = form.cleaned_data.get(
            "hiq_foto_kryesore",
            False
        )

        banesa_e_vjeter = None
        numri_ekzistues = 0

        if self.object is not None and self.object.pk:
            banesa_e_vjeter = (
                Banesa.objects.select_for_update().get(
                    pk=self.object.pk
                )
            )

            numri_ekzistues = (
                FotografiaBaneses.objects.filter(
                    banesa=banesa_e_vjeter
                ).count()
            )

        numri_perfundimtar = (
            numri_ekzistues
            - len(fotot_per_fshirje)
            + len(fotot_e_reja)
        )

        if numri_perfundimtar > 7:
            form.add_error(
                "fotot_shtese",
                "Një banesë mund të ketë maksimumi 7 fotografi shtesë."
            )
            return self.form_invalid(form)

        foto_kryesore_e_vjeter = None

        if banesa_e_vjeter and banesa_e_vjeter.fotografia:
            foto_kryesore_e_vjeter = (
                banesa_e_vjeter.fotografia
            )

        response = super().form_valid(form)

        if hiq_foto_kryesore:
            self.object.fotografia = ""
            self.object.save(
                update_fields=["fotografia"]
            )

        if foto_kryesore_e_vjeter:
            emri_i_ri = (
                self.object.fotografia.name
                if self.object.fotografia
                else ""
            )

            if foto_kryesore_e_vjeter.name != emri_i_ri:
                self.planifiko_fshirjen_e_skedarit(
                    foto_kryesore_e_vjeter
                )

        if fotot_per_fshirje:
            identifikuesit = [
                foto.pk for foto in fotot_per_fshirje
            ]

            fotografite = list(
                FotografiaBaneses.objects.filter(
                    banesa=self.object,
                    pk__in=identifikuesit
                )
            )

            for foto in fotografite:
                self.planifiko_fshirjen_e_skedarit(
                    foto.fotografia
                )

            FotografiaBaneses.objects.filter(
                banesa=self.object,
                pk__in=identifikuesit
            ).delete()

        renditja_tjeter = (
            FotografiaBaneses.objects.filter(
                banesa=self.object
            ).aggregate(
                maksimumi=Max("renditja")
            )["maksimumi"] or 0
        ) + 1

        for foto in fotot_e_reja:
            FotografiaBaneses.objects.create(
                banesa=self.object,
                fotografia=foto,
                pershkrimi="",
                renditja=renditja_tjeter
            )

            renditja_tjeter += 1

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