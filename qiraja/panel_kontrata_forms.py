from django import forms

from .models import Kontrata
from .panel_forms import StiliFormes


class KontrataForm(StiliFormes, forms.ModelForm):

    class Meta:
        model = Kontrata

        fields = [
            "banesa",
            "qiramarresi",
            "data_fillimit",
            "data_mbarimit",
            "qiraja_mujore",
        ]

        labels = {
            "banesa": "Banesa",
            "qiramarresi": "Qiramarrësi",
            "data_fillimit": "Data e fillimit",
            "data_mbarimit": "Data e mbarimit",
            "qiraja_mujore": "Qiraja mujore (€)",
        }

        widgets = {
            "banesa": forms.Select(),
            "qiramarresi": forms.Select(),
            "data_fillimit": forms.DateInput(
                format="%Y-%m-%d",
                attrs={"type": "date"}
            ),
            "data_mbarimit": forms.DateInput(
                format="%Y-%m-%d",
                attrs={"type": "date"}
            ),
            "qiraja_mujore": forms.NumberInput(
                attrs={
                    "min": "0.01",
                    "step": "0.01",
                    "placeholder": "Shkruaj qiranë mujore"
                }
            ),
        }

    def clean(self):
        cleaned_data = super().clean()

        banesa = cleaned_data.get("banesa")
        data_fillimit = cleaned_data.get("data_fillimit")
        data_mbarimit = cleaned_data.get("data_mbarimit")
        qiraja_mujore = cleaned_data.get("qiraja_mujore")

        if data_fillimit and data_mbarimit:

            if data_mbarimit <= data_fillimit:
                self.add_error(
                    "data_mbarimit",
                    "Data e mbarimit duhet të jetë pas datës së fillimit."
                )

            elif banesa:

                kontratat = Kontrata.objects.filter(
                    banesa=banesa,
                    status="aktive",
                    data_fillimit__lte=data_mbarimit,
                    data_mbarimit__gte=data_fillimit
                )

                if self.instance.pk:
                    kontratat = kontratat.exclude(
                        pk=self.instance.pk
                    )

                if kontratat.exists():
                    self.add_error(
                        "banesa",
                        "Kjo banesë ka një kontratë tjetër "
                        "aktive për periudhën e zgjedhur."
                    )

        if qiraja_mujore is not None and qiraja_mujore <= 0:
            self.add_error(
                "qiraja_mujore",
                "Qiraja mujore duhet të jetë më e madhe se zero."
            )

        return cleaned_data