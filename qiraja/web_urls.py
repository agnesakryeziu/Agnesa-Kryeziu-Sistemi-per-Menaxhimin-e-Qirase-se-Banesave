from django.urls import path
from . import web_views

urlpatterns = [
    path("", web_views.home, name="home"),
    path("banesat/", web_views.banesat, name="banesat"),
    path(
        "banesat/<int:pk>/",
        web_views.detajet_baneses,
        name="detajet_baneses"
    ),
]
