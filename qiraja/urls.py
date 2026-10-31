from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    PronariViewSet,
    BanesaViewSet,
    QiramarresiViewSet,
    KontrataViewSet,
    PagesaViewSet,
)

router = DefaultRouter()

router.register("pronaret", PronariViewSet)
router.register("banesat", BanesaViewSet)
router.register("qiramarresit", QiramarresiViewSet)
router.register("kontratat", KontrataViewSet)
router.register("pagesat", PagesaViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
