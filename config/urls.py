from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from qiraja.panel_delete_views import (
    FshiBanese,
    FshiPronar,
    FshiQiramarres,
)

from qiraja.panel_kontrata_cancel_views import AnuloKontrate
from qiraja.panel_pronari_views import PaneliPronarit
from qiraja.rezervimi_views import RezervoBanese

from qiraja.pronari_rezervimet_views import (
    ListaRezervimevePronari,
    VendimiRezervimit,
)

from qiraja.pronari_banesat_views import (
    ShtoBanesePronari,
    NdryshoBanesePronari,
)

from qiraja.pronari_faqet_views import (
    BanesatPronarit,
    KontratatPronarit,
    PagesatPronarit,
    ProfiliPronarit,
)

from qiraja.rezervimet_pasqyra_views import (
    RezervimetKlientit,
    RezervimetAdministratorit,
)

from qiraja.panel_kontrata_views import (
    ListaKontratave,
    ShtoKontrate,
    NdryshoKontrate,
)

from qiraja.panel_pagesa_views import (
    ListaPagesave,
    ShtoPagese,
    NdryshoPagese,
)


urlpatterns = [

    path("admin/", admin.site.urls),
    path("api/", include("qiraja.urls")),
    path("api-auth/", include("rest_framework.urls")),

    path(
        "pronari/",
        PaneliPronarit.as_view(),
        name="paneli_pronarit"
    ),

    path(
        "pronari/banesat/",
        BanesatPronarit.as_view(),
        name="pronari_banesat"
    ),

    path(
        "pronari/banesat/shto/",
        ShtoBanesePronari.as_view(),
        name="pronari_shto_banese"
    ),

    path(
        "pronari/banesat/<int:pk>/ndrysho/",
        NdryshoBanesePronari.as_view(),
        name="pronari_ndrysho_banese"
    ),

    path(
        "pronari/rezervimet/",
        ListaRezervimevePronari.as_view(),
        name="pronari_rezervimet"
    ),

    path(
        "pronari/rezervimet/<int:pk>/vendimi/",
        VendimiRezervimit.as_view(),
        name="pronari_vendimi_rezervimit"
    ),

    path(
        "pronari/kontratat/",
        KontratatPronarit.as_view(),
        name="pronari_kontratat"
    ),

    path(
        "pronari/pagesat/",
        PagesatPronarit.as_view(),
        name="pronari_pagesat"
    ),

    path(
        "pronari/profili/",
        ProfiliPronarit.as_view(),
        name="pronari_profili"
    ),

    path(
        "banesat/<int:pk>/rezervo/",
        RezervoBanese.as_view(),
        name="rezervo_banese"
    ),

    path(
        "rezervimet-e-mia/",
        RezervimetKlientit.as_view(),
        name="klienti_rezervimet"
    ),

    path(
        "paneli/rezervimet/",
        RezervimetAdministratorit.as_view(),
        name="panel_rezervimet"
    ),

    path(
        "paneli/banesat/<int:pk>/fshi/",
        FshiBanese.as_view(),
        name="panel_fshi_banese"
    ),

    path(
        "paneli/pronaret/<int:pk>/fshi/",
        FshiPronar.as_view(),
        name="panel_fshi_pronar"
    ),

    path(
        "paneli/qiramarresit/<int:pk>/fshi/",
        FshiQiramarres.as_view(),
        name="panel_fshi_qiramarres"
    ),

    path(
        "paneli/kontratat/",
        ListaKontratave.as_view(),
        name="panel_kontratat"
    ),

    path(
        "paneli/kontratat/shto/",
        ShtoKontrate.as_view(),
        name="panel_shto_kontrate"
    ),

    path(
        "paneli/kontratat/<int:pk>/ndrysho/",
        NdryshoKontrate.as_view(),
        name="panel_ndrysho_kontrate"
    ),

    path(
        "paneli/kontratat/<int:pk>/anulo/",
        AnuloKontrate.as_view(),
        name="panel_anulo_kontrate"
    ),

    path(
        "paneli/pagesat/",
        ListaPagesave.as_view(),
        name="panel_pagesat"
    ),

    path(
        "paneli/pagesat/shto/",
        ShtoPagese.as_view(),
        name="panel_shto_pagese"
    ),

    path(
        "paneli/pagesat/<int:pk>/ndrysho/",
        NdryshoPagese.as_view(),
        name="panel_ndrysho_pagese"
    ),

    path("", include("qiraja.web_urls")),
]


if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )