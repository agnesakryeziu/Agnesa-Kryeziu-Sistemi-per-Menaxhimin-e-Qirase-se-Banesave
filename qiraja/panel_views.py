from datetime import timedelta
from decimal import Decimal

from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.http import HttpResponseForbidden
from django.shortcuts import render
from django.utils import timezone

from .models import Banesa, Pronari, Qiramarresi, Kontrata, Pagesa


@login_required(login_url="hyrja")
def paneli(request):
    if not request.user.is_staff:
        return HttpResponseForbidden(
            "Nuk keni leje për të hapur këtë panel."
        )

    sot = timezone.localdate()

    kontratat_aktive = Kontrata.objects.filter(
        status="aktive",
        data_fillimit__lte=sot,
        data_mbarimit__gte=sot
    )

    banesat_gjithsej = Banesa.objects.count()

    banesat_e_zena = kontratat_aktive.values(
        "banesa_id"
    ).distinct().count()

    banesat_e_lira = max(
        banesat_gjithsej - banesat_e_zena,
        0
    )

    pagesat_kete_muaj = Pagesa.objects.filter(
        muaji=sot.month,
        viti=sot.year
    ).count()

    pagesat_e_paguara = Pagesa.objects.filter(
        e_paguar=True
    ).count()

    pagesat_e_papaguara = Pagesa.objects.filter(
        e_paguar=False
    ).count()

    kontratat_ne_skadim = kontratat_aktive.filter(
        data_mbarimit__lte=sot + timedelta(days=30)
    ).count()

    kontratat_e_fundit = Kontrata.objects.select_related(
        "banesa",
        "qiramarresi"
    ).order_by("-data_fillimit", "-id")[:5]

    pagesat_e_fundit = Pagesa.objects.select_related(
        "kontrata",
        "kontrata__banesa",
        "kontrata__qiramarresi"
    ).order_by("-data_pageses", "-id")[:5]

    emrat_e_muajve = [
        "Jan", "Shk", "Mar", "Pri", "Maj", "Qer",
        "Kor", "Gus", "Sht", "Tet", "Nen", "Dhj"
    ]

    muajt = []

    for largesia in range(5, -1, -1):
        numri_absolut = (
            sot.year * 12 + sot.month - 1 - largesia
        )

        viti, muaji_zero = divmod(numri_absolut, 12)
        muaji = muaji_zero + 1

        shuma = Pagesa.objects.filter(
            e_paguar=True,
            data_pageses__year=viti,
            data_pageses__month=muaji
        ).aggregate(
            totali=Sum("shuma")
        )["totali"] or Decimal("0.00")

        muajt.append({
            "emri": emrat_e_muajve[muaji - 1],
            "viti": viti,
            "shuma": shuma
        })

    shumat = [float(muaji["shuma"]) for muaji in muajt]
    shuma_maksimale = max(shumat, default=0)
    shkalla = max(shuma_maksimale, 1)

    pikat = []

    for indeksi, muaji in enumerate(muajt):
        x = 35 + indeksi * 128
        y = 175 - (float(muaji["shuma"]) / shkalla) * 135

        pikat.append({
            "x": str(x),
            "y": f"{y:.1f}",
            "emri": muaji["emri"],
            "shuma": muaji["shuma"]
        })

    grafiku_pikat = " ".join(
        f'{pika["x"]},{pika["y"]}'
        for pika in pikat
    )

    grafiku_zona = (
        f"35,175 {grafiku_pikat} 675,175"
    )

    context = {
        "sot": sot,
        "banesat_gjithsej": banesat_gjithsej,
        "banesat_e_lira": banesat_e_lira,
        "banesat_e_zena": banesat_e_zena,
        "pronaret_gjithsej": Pronari.objects.count(),
        "qiramarresit_gjithsej": Qiramarresi.objects.count(),
        "kontratat_aktive": kontratat_aktive.count(),
        "kontratat_ne_skadim": kontratat_ne_skadim,
        "pagesat_kete_muaj": pagesat_kete_muaj,
        "pagesat_e_paguara": pagesat_e_paguara,
        "pagesat_e_papaguara": pagesat_e_papaguara,
        "kontratat_e_fundit": kontratat_e_fundit,
        "pagesat_e_fundit": pagesat_e_fundit,
        "grafiku_pikat": grafiku_pikat,
        "grafiku_zona": grafiku_zona,
        "grafiku_muajt": pikat,
        "grafiku_maks": shuma_maksimale,
        "grafiku_gjysma": shuma_maksimale / 2,
        "ka_te_hyra": shuma_maksimale > 0
    }

    return render(
        request,
        "qiraja/paneli.html",
        context
    )
