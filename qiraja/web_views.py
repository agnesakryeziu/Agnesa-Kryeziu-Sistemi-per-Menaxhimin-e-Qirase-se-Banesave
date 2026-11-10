from decimal import Decimal, InvalidOperation

from django.db.models import Exists, OuterRef, Q
from django.shortcuts import render
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