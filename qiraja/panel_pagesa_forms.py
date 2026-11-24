from django import forms

from .models import Pagesa
from .panel_forms import StiliFormes


class PagesaForm(StiliFormes, forms.ModelForm):

    MUAJT = [
        ("", "Zgjidh muajin"),
        (1, "Janar"),
        (2, "Shkurt"),
        (3, "Mars"),
        (4, "Prill"),
        (5, "Maj"),
        (6, "Qershor"),
        (7, "Korrik"),
        (8, "Gusht"),
        (9, "Shtator"),
        (10, "Tetor"),
        (11, "Nëntor"),
        (12, "Dhjetor"),
    ]

    muaji = forms.TypedChoiceField(
        choices=MUAJT,
        coerce=int,
        label="Muaji",
    )

    class Meta:
        model = Pagesa

        fields = [
            "kontrata",
            "muaji",
            "viti",
            "shuma",
            "data_pageses",
            "e_paguar",
        ]

        labels = {
            "kontrata": "Kontrata",
            "viti": "Viti",
            "shuma": "Shuma (€)",
            "data_pageses": "Data e pagesës",
            "e_paguar": "Pagesa është realizuar",
        }

        widgets = {
            "kontrata": forms.Select(),

            "viti": forms.NumberInput(
                attrs={
                    "min": "2000",
                    "max": "9999",
                    "placeholder": "P.sh. 2026",
                }
            ),

            "shuma": forms.NumberInput(
                attrs={
                    "min": "0.01",
                    "step": "0.01",
                    "placeholder": "Shuma në euro",
                }
            ),

            "data_pageses": forms.DateInput(
                format="%Y-%m-%d",
                attrs={
                    "type": "date",
                }
            ),

            "e_paguar": forms.CheckboxInput(),
        }

    def clean(self):
        cleaned_data = super().clean()

        muaji = cleaned_data.get("muaji")
        viti = cleaned_data.get("viti")
        shuma = cleaned_data.get("shuma")
        kontrata = cleaned_data.get("kontrata")

        if shuma is not None and shuma <= 0:
            self.add_error(
                "shuma",
                "Shuma duhet të jetë më e madhe se zero."
            )

        if viti is not None and viti < 2000:
            self.add_error(
                "viti",
                "Viti nuk është i vlefshëm."
            )

        if kontrata and muaji and viti:

            pagesat = Pagesa.objects.filter(
                kontrata=kontrata,
                muaji=muaji,
                viti=viti,
            )

            if self.instance.pk:
                pagesat = pagesat.exclude(
                    pk=self.instance.pk
                )

            if pagesat.exists():
                self.add_error(
                    "muaji",
                    "Për këtë kontratë ekziston tashmë "
                    "një pagesë për muajin dhe vitin e zgjedhur."
                )

        return cleaned_data