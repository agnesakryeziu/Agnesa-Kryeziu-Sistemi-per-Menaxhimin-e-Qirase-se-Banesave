from decimal import Decimal, InvalidOperation

from django.db.models import Exists, OuterRef, Q
from django.shortcuts import get_object_or_404, render
from django.utils import timezone

from .models import Banesa, Kontrata


def home(request):
    sot = timezone.localdate()

    kontratat_aktive = Kontrata.objects.filter(
        banesa_id=OuterRef("pk"),
        data_fillimit__lte=sot,
        data_mbarimit__gte=sot
    )

    banesat = Banesa.objects.annotate(
        e_zene=Exists(kontratat_aktive)
    ).order_by("-id")

    kerkimi = request.GET.get("q", "").strip()
    qyteti = request.GET.get("qyteti", "").strip()
    cmimi_max = request.GET.get("cmimi_max", "").strip()

    if kerkimi:
        banesat = banesat.filter(
            Q(adresa__icontains=kerkimi) |
            Q(qyteti__icontains=kerkimi)
        )

    if qyteti:
        banesat = banesat.filter(
            qyteti__iexact=qyteti
        )

    if cmimi_max:
        try:
            cmimi = Decimal(cmimi_max)

            if (
                not cmimi.is_finite()
                or cmimi < 0
                or cmimi > Decimal("99999999.99")
            ):
                raise InvalidOperation

            banesat = banesat.filter(
                cmimi_mujor__lte=cmimi
            )

        except InvalidOperation:
            banesat = banesat.none()

    context = {
        "banesat": banesat[:3]
    }

    return render(
        request,
        "qiraja/home.html",
        context
    )


def banesat(request):
    sot = timezone.localdate()

    kontratat_aktive = Kontrata.objects.filter(
        banesa_id=OuterRef("pk"),
        data_fillimit__lte=sot,
        data_mbarimit__gte=sot
    )

    banesat_qs = Banesa.objects.annotate(
        e_zene=Exists(kontratat_aktive)
    )

    kerkimi = request.GET.get("q", "").strip()
    qyteti = request.GET.get("qyteti", "").strip()
    cmimi_max = request.GET.get("cmimi_max", "").strip()
    statusi = request.GET.get("statusi", "").strip()
    renditja = request.GET.get("renditja", "fundit")
    gabim_filtri = ""

    if kerkimi:
        banesat_qs = banesat_qs.filter(
            Q(adresa__icontains=kerkimi) |
            Q(qyteti__icontains=kerkimi)
        )

    if qyteti:
        banesat_qs = banesat_qs.filter(
            qyteti__iexact=qyteti
        )

    if cmimi_max:
        try:
            cmimi = Decimal(cmimi_max)

            if (
                not cmimi.is_finite()
                or cmimi < 0
                or cmimi > Decimal("99999999.99")
            ):
                raise InvalidOperation

            banesat_qs = banesat_qs.filter(
                cmimi_mujor__lte=cmimi
            )

        except InvalidOperation:
            gabim_filtri = "Çmimi maksimal nuk është i vlefshëm."
            banesat_qs = banesat_qs.none()

    if statusi == "lire":
        banesat_qs = banesat_qs.filter(e_zene=False)

    elif statusi == "zene":
        banesat_qs = banesat_qs.filter(e_zene=True)

    if renditja == "cmimi_ulte":
        banesat_qs = banesat_qs.order_by(
            "cmimi_mujor", "-id"
        )

    elif renditja == "cmimi_larte":
        banesat_qs = banesat_qs.order_by(
            "-cmimi_mujor", "-id"
        )

    else:
        renditja = "fundit"
        banesat_qs = banesat_qs.order_by("-id")

    qytetet = Banesa.objects.order_by(
        "qyteti"
    ).values_list(
        "qyteti", flat=True
    ).distinct()

    context = {
        "banesat": banesat_qs,
        "qytetet": qytetet,
        "kerkimi": kerkimi,
        "qyteti_zgjedhur": qyteti,
        "cmimi_max": cmimi_max,
        "statusi": statusi,
        "renditja": renditja,
        "gabim_filtri": gabim_filtri,
        "numri_rezultateve": banesat_qs.count()
    }

    return render(
        request,
        "qiraja/banesat.html",
        context
    )


def detajet_baneses(request, pk):
    sot = timezone.localdate()

    kontratat_aktive = Kontrata.objects.filter(
        banesa_id=OuterRef("pk"),
        data_fillimit__lte=sot,
        data_mbarimit__gte=sot
    )

    banesa = get_object_or_404(
        Banesa.objects.annotate(
            e_zene=Exists(kontratat_aktive)
        ),
        pk=pk
    )

    return render(
        request,
        "qiraja/detajet_baneses.html",
        {"banesa": banesa}
    )
