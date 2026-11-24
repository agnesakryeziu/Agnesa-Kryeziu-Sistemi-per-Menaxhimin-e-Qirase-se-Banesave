from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path as delete_path
from qiraja.panel_delete_views import FshiBanese
from qiraja.panel_delete_views import FshiPronar, FshiQiramarres
from qiraja.panel_kontrata_cancel_views import AnuloKontrate


urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("qiraja.urls")),
    path("api-auth/", include("rest_framework.urls")),
    path("", include("qiraja.web_urls")),
]


if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )

urlpatterns += [
    delete_path(
        "paneli/banesat/<int:pk>/fshi/",
        FshiBanese.as_view(),
        name="panel_fshi_banese"
    ),
]
urlpatterns += [
    delete_path(
        "paneli/pronaret/<int:pk>/fshi/",
        FshiPronar.as_view(),
        name="panel_fshi_pronar"
    ),
    delete_path(
        "paneli/qiramarresit/<int:pk>/fshi/",
        FshiQiramarres.as_view(),
        name="panel_fshi_qiramarres"
    ),
]
urlpatterns += [
    delete_path(
        "paneli/kontratat/<int:pk>/anulo/",
        AnuloKontrate.as_view(),
        name="panel_anulo_kontrate"
    ),
]


from django.urls import path as kontrata_path
from qiraja.panel_kontrata_views import (
    ListaKontratave,
    ShtoKontrate,
    NdryshoKontrate,
)

urlpatterns += [
    kontrata_path(
        "paneli/kontratat/",
        ListaKontratave.as_view(),
        name="panel_kontratat"
    ),
    kontrata_path(
        "paneli/kontratat/shto/",
        ShtoKontrate.as_view(),
        name="panel_shto_kontrate"
    ),
    kontrata_path(
        "paneli/kontratat/<int:pk>/ndrysho/",
        NdryshoKontrate.as_view(),
        name="panel_ndrysho_kontrate"
    ),
]
