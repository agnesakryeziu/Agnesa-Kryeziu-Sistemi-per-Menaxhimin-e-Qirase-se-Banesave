from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path as delete_path
from qiraja.panel_delete_views import FshiBanese
from qiraja.panel_delete_views import FshiPronar, FshiQiramarres


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
