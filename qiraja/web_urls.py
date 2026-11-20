from django.urls import path

from . import web_views
from .kontakt_views import KontaktView
from .login_views import HyrjeView, DaljeView


urlpatterns = [
    path(
        "",
        web_views.home,
        name="home"
    ),
    path(
        "banesat/",
        web_views.banesat,
        name="banesat"
    ),
    path(
        "banesat/<int:pk>/",
        web_views.detajet_baneses,
        name="detajet_baneses"
    ),
    path(
        "rreth-nesh/",
        web_views.rreth_nesh,
        name="rreth_nesh"
    ),
    path(
        "sherbimet/",
        web_views.sherbimet,
        name="sherbimet"
    ),
    path(
        "kontaktet/",
        KontaktView.as_view(),
        name="kontaktet"
    ),
    path(
        "hyrja/",
        HyrjeView.as_view(),
        name="hyrja"
    ),
    path(
        "dalje/",
        DaljeView.as_view(),
        name="dalje"
    ),
]
