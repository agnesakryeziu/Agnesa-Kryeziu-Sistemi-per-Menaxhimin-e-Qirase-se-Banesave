from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser

from .models import (
    Pronari,
    Banesa,
    Qiramarresi,
    Kontrata,
    Pagesa,
)

from .serializers import (
    PronariSerializer,
    BanesaSerializer,
    QiramarresiSerializer,
    KontrataSerializer,
    PagesaSerializer,
)


class PronariViewSet(viewsets.ModelViewSet):
    queryset = Pronari.objects.all()
    serializer_class = PronariSerializer
    permission_classes = [IsAdminUser]


class BanesaViewSet(viewsets.ModelViewSet):
    queryset = Banesa.objects.all()
    serializer_class = BanesaSerializer
    permission_classes = [IsAdminUser]


class QiramarresiViewSet(viewsets.ModelViewSet):
    queryset = Qiramarresi.objects.all()
    serializer_class = QiramarresiSerializer
    permission_classes = [IsAdminUser]


class KontrataViewSet(viewsets.ModelViewSet):
    queryset = Kontrata.objects.all()
    serializer_class = KontrataSerializer
    permission_classes = [IsAdminUser]


class PagesaViewSet(viewsets.ModelViewSet):
    queryset = Pagesa.objects.all()
    serializer_class = PagesaSerializer
    permission_classes = [IsAdminUser]