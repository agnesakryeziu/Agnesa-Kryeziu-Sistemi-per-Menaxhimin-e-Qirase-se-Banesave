from django import forms

from .models import Banesa


class BanesaPronaritForm(forms.ModelForm):

    class Meta:
        model = Banesa

        fields = [
            "adresa",
            "qyteti",
            "siperfaqja",
            "numri_dhomave",
            "cmimi_mujor",
            "fotografia",
        ]

        labels = {
            "adresa": "Adresa",
            "qyteti": "Qyteti",
            "siperfaqja": "Sipërfaqja (m²)",
            "numri_dhomave": "Numri i dhomave",
            "cmimi_mujor": "Qiraja mujore (€)",
            "fotografia": "Fotografia e banesës",
        }

        widgets = {
            "adresa": forms.TextInput(attrs={
                "placeholder": "Shkruani adresën e banesës"
            }),

            "qyteti": forms.TextInput(attrs={
                "placeholder": "Shkruani qytetin"
            }),

            "siperfaqja": forms.NumberInput(attrs={
                "placeholder": "P.sh. 85",
                "min": 1
            }),

            "numri_dhomave": forms.NumberInput(attrs={
                "placeholder": "P.sh. 3",
                "min": 1
            }),

            "cmimi_mujor": forms.NumberInput(attrs={
                "placeholder": "P.sh. 350",
                "min": "0.01",
                "step": "0.01"
            }),

            "fotografia": forms.ClearableFileInput(attrs={
                "accept": "image/jpeg,image/png,image/webp"
            }),
        }

    def clean_siperfaqja(self):
        siperfaqja = self.cleaned_data["siperfaqja"]

        if siperfaqja <= 0:
            raise forms.ValidationError(
                "Sipërfaqja duhet të jetë më e madhe se zero."
            )

        return siperfaqja

    def clean_numri_dhomave(self):
        numri = self.cleaned_data["numri_dhomave"]

        if numri <= 0:
            raise forms.ValidationError(
                "Numri i dhomave duhet të jetë më i madh se zero."
            )

        return numri

    def clean_cmimi_mujor(self):
        cmimi = self.cleaned_data["cmimi_mujor"]

        if cmimi <= 0:
            raise forms.ValidationError(
                "Qiraja mujore duhet të jetë më e madhe se zero."
            )

        return cmimi