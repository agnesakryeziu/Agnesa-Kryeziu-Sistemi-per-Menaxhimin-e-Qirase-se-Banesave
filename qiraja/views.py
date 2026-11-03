from django.db.models.deletion import ProtectedError
from rest_framework import status, viewsets
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response

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
class ViewSetMeMbrojtje(viewsets.ModelViewSet):
    permission_classes = [IsAdminUser]

    def destroy(self, request, *args, **kwargs):
        objekti = self.get_object()

        try:
            self.perform_destroy(objekti)
        except ProtectedError:
            return Response(
                {
                    "error": "Fshirja nuk lejohet.",
                    "message": (
                        "Ekzistojne te dhena te lidhura "
                        "me kete rekord."
                    ),
                },
                status=status.HTTP_409_CONFLICT
            )

        return Response(
            status=status.HTTP_204_NO_CONTENT
        )


class PronariViewSet(ViewSetMeMbrojtje):
    queryset = Pronari.objects.all()
    serializer_class = PronariSerializer


class BanesaViewSet(ViewSetMeMbrojtje):
    queryset = Banesa.objects.all()
    serializer_class = BanesaSerializer


class QiramarresiViewSet(ViewSetMeMbrojtje):
    queryset = Qiramarresi.objects.all()
    serializer_class = QiramarresiSerializer


class KontrataViewSet(ViewSetMeMbrojtje):
    queryset = Kontrata.objects.all()
    serializer_class = KontrataSerializer


class PagesaViewSet(ViewSetMeMbrojtje):
    queryset = Pagesa.objects.all()
    serializer_class = PagesaSerializer