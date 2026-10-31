from rest_framework import serializers
from django.core.exceptions import ValidationError as DjangoValidationError

from .models import (
    Pronari,
    Banesa,
    Qiramarresi,
    Kontrata,
    Pagesa,
)


class ValidimModeliSerializer(serializers.ModelSerializer):
    def validate(self, attrs):
        te_dhenat = {}

        if self.instance:
         for fusha in self.Meta.model._meta.fields:
            if fusha.name != "id":
                te_dhenat[fusha.name] = getattr(
                    self.instance, fusha.name
                )

        te_dhenat.update(attrs)

        objekti = self.Meta.model(**te_dhenat)

        if self.instance:
            objekti.pk = self.instance.pk
            objekti._state.adding = False


        try:
            objekti.full_clean()
        except DjangoValidationError as gabim:
            if hasattr(gabim, "message_dict"):
                raise serializers.ValidationError(gabim.message_dict)
            raise serializers.ValidationError(gabim.messages)

        return attrs


class PronariSerializer(ValidimModeliSerializer):
    class Meta:
        model = Pronari
        fields = "__all__"


class BanesaSerializer(ValidimModeliSerializer):
    class Meta:
        model = Banesa
        fields = "__all__"


class QiramarresiSerializer(ValidimModeliSerializer):
    class Meta:
        model = Qiramarresi
        fields = "__all__"


class KontrataSerializer(ValidimModeliSerializer):
    class Meta:
        model = Kontrata
        fields = "__all__"


class PagesaSerializer(ValidimModeliSerializer):
    class Meta:
        model = Pagesa
        fields = "__all__"