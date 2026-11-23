from django import forms

from .models import Banesa, Pronari, Qiramarresi, FotografiaBaneses


class MultipleImageInput(forms.ClearableFileInput):
    allow_multiple_selected = True


class MultipleImageField(forms.ImageField):
    widget = MultipleImageInput

    def clean(self, data, initial=None):
        if not data:
            return []

        if not isinstance(data, (list, tuple)):
            data = [data]

        if len(data) > 7:
            raise forms.ValidationError(
                "Mund të ngarkoni maksimumi 7 fotografi shtesë."
            )

        return [
            super(MultipleImageField, self).clean(foto)
            for foto in data
        ]


class StiliFormes:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for fusha in self.fields.values():
            fusha.widget.attrs["class"] = "rmp-form-input"


class BanesaForm(StiliFormes, forms.ModelForm):
    fotot_shtese = MultipleImageField(
        required=False,
        label="Fotografi shtesë",
        help_text="Mund të zgjidhni deri në 7 fotografi shtesë.",
        widget=MultipleImageInput(
            attrs={
                "accept": "image/*",
                "multiple": True,
            }
        ),
    )

    hiq_foto_kryesore = forms.BooleanField(
        required=False,
        label="Largo fotografinë kryesore",
    )

    fotot_per_fshirje = forms.ModelMultipleChoiceField(
        queryset=FotografiaBaneses.objects.none(),
        required=False,
        widget=forms.CheckboxSelectMultiple,
        label="Fotografitë për largim",
    )

    class Meta:
        model = Banesa

        fields = [
            "adresa",
            "qyteti",
            "siperfaqja",
            "numri_dhomave",
            "cmimi_mujor",
            "fotografia",
            "pronari",
        ]

        labels = {
            "adresa": "Adresa",
            "qyteti": "Qyteti",
            "siperfaqja": "Sipërfaqja (m²)",
            "numri_dhomave": "Numri i dhomave",
            "cmimi_mujor": "Qiraja mujore (€)",
            "fotografia": "Fotografia kryesore",
            "pronari": "Pronari",
        }

        widgets = {
            "adresa": forms.TextInput(
                attrs={"placeholder": "Shkruaj adresën"}
            ),
            "qyteti": forms.TextInput(
                attrs={"placeholder": "Shkruaj qytetin"}
            ),
            "siperfaqja": forms.NumberInput(
                attrs={"min": "1"}
            ),
            "numri_dhomave": forms.NumberInput(
                attrs={"min": "1"}
            ),
            "cmimi_mujor": forms.NumberInput(
                attrs={"min": "0.01", "step": "0.01"}
            ),
            "fotografia": forms.ClearableFileInput(
                attrs={"accept": "image/*"}
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if self.instance and self.instance.pk:
            self.fields["fotot_per_fshirje"].queryset = (
                FotografiaBaneses.objects.filter(
                    banesa=self.instance
                )
            )

    def clean(self):
        cleaned_data = super().clean()

        fotot_e_reja = cleaned_data.get("fotot_shtese") or []
        fotot_per_fshirje = (
            cleaned_data.get("fotot_per_fshirje") or []
        )

        if self.instance and self.instance.pk:
            numri_ekzistues = (
                self.instance.fotografite.count()
            )
        else:
            numri_ekzistues = 0

        numri_perfundimtar = (
            numri_ekzistues
            - len(fotot_per_fshirje)
            + len(fotot_e_reja)
        )

        if numri_perfundimtar > 7:
            self.add_error(
                "fotot_shtese",
                "Një banesë mund të ketë maksimumi 7 fotografi shtesë."
            )

        if (
            cleaned_data.get("hiq_foto_kryesore")
            and self.files.get("fotografia")
        ):
            self.add_error(
                "fotografia",
                "Zgjidhni ose largimin ose zëvendësimin e fotografisë kryesore."
            )

        return cleaned_data


class PronariForm(StiliFormes, forms.ModelForm):
    class Meta:
        model = Pronari

        fields = [
            "emri",
            "mbiemri",
            "telefoni",
            "email",
        ]

        labels = {
            "emri": "Emri",
            "mbiemri": "Mbiemri",
            "telefoni": "Telefoni",
            "email": "Email",
        }

        widgets = {
            "emri": forms.TextInput(
                attrs={"placeholder": "Shkruaj emrin"}
            ),
            "mbiemri": forms.TextInput(
                attrs={"placeholder": "Shkruaj mbiemrin"}
            ),
            "telefoni": forms.TextInput(
                attrs={"placeholder": "+383"}
            ),
            "email": forms.EmailInput(
                attrs={"placeholder": "emri@email.com"}
            ),
        }


class QiramarresiForm(StiliFormes, forms.ModelForm):
    class Meta:
        model = Qiramarresi

        fields = [
            "emri",
            "mbiemri",
            "telefoni",
            "email",
        ]

        labels = {
            "emri": "Emri",
            "mbiemri": "Mbiemri",
            "telefoni": "Telefoni",
            "email": "Email",
        }

        widgets = {
            "emri": forms.TextInput(
                attrs={"placeholder": "Shkruaj emrin"}
            ),
            "mbiemri": forms.TextInput(
                attrs={"placeholder": "Shkruaj mbiemrin"}
            ),
            "telefoni": forms.TextInput(
                attrs={"placeholder": "+383"}
            ),
            "email": forms.EmailInput(
                attrs={"placeholder": "emri@email.com"}
            ),
        }
