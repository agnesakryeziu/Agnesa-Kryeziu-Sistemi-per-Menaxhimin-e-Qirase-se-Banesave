from django.urls import path

from . import web_views
from .kontakt_views import KontaktView
from .login_views import HyrjeView, DaljeView
from .panel_views import paneli

from .panel_management_views import (
    ListaBanesave,
    ListaPronareve,
    ListaQiramarresve,
    ShtoBanese,
    NdryshoBanese,
    ShtoPronar,
    NdryshoPronar,
    ShtoQiramarres,
    NdryshoQiramarres,
)


urlpatterns = [
    path("", web_views.home, name="home"),

    path(
        "banesat/",
        web_views.banesat,
        name="banesat",
    ),

    path(
        "banesat/<int:pk>/",
        web_views.detajet_baneses,
        name="detajet_baneses",
    ),

    path(
        "rreth-nesh/",
        web_views.rreth_nesh,
        name="rreth_nesh",
    ),

    path(
        "sherbimet/",
        web_views.sherbimet,
        name="sherbimet",
    ),

    path(
        "kontaktet/",
        KontaktView.as_view(),
        name="kontaktet",
    ),

    path(
        "hyrja/",
        HyrjeView.as_view(),
        name="hyrja",
    ),

    path(
        "dalje/",
        DaljeView.as_view(),
        name="dalje",
    ),

    path(
        "paneli/",
        paneli,
        name="paneli",
    ),

    path(
        "paneli/banesat/",
        ListaBanesave.as_view(),
        name="panel_banesat",
    ),

    path(
        "paneli/banesat/shto/",
        ShtoBanese.as_view(),
        name="panel_shto_banese",
    ),

    path(
        "paneli/banesat/<int:pk>/ndrysho/",
        NdryshoBanese.as_view(),
        name="panel_ndrysho_banese",
    ),

    path(
        "paneli/pronaret/",
        ListaPronareve.as_view(),
        name="panel_pronaret",
    ),

    path(
        "paneli/pronaret/shto/",
        ShtoPronar.as_view(),
        name="panel_shto_pronar",
    ),

    path(
        "paneli/pronaret/<int:pk>/ndrysho/",
        NdryshoPronar.as_view(),
        name="panel_ndrysho_pronar",
    ),

    path(
        "paneli/qiramarresit/",
        ListaQiramarresve.as_view(),
        name="panel_qiramarresit",
    ),

    path(
        "paneli/qiramarresit/shto/",
        ShtoQiramarres.as_view(),
        name="panel_shto_qiramarres",
    ),

    path(
        "paneli/qiramarresit/<int:pk>/ndrysho/",
        NdryshoQiramarres.as_view(),
        name="panel_ndrysho_qiramarres",
    ),
]