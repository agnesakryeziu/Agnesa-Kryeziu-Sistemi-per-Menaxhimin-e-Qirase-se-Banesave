from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.db import transaction

from .models import Pronari


class RegjistrimiForm(forms.Form):

    ROLET = [
        ("klient", "Jam klient"),
        ("pronar", "Jam pronar"),
    ]

    roli = forms.ChoiceField(
        choices=ROLET,
        initial="klient",
        required=False,
        label="Lloji i llogarisë"
    )

    emri = forms.CharField(
        max_length=150,
        label="Emri",
        widget=forms.TextInput(
            attrs={"placeholder": "Shkruaj emrin"}
        )
    )

    mbiemri = forms.CharField(
        max_length=150,
        label="Mbiemri",
        widget=forms.TextInput(
            attrs={"placeholder": "Shkruaj mbiemrin"}
        )
    )

    email = forms.EmailField(
        label="Email",
        widget=forms.EmailInput(
            attrs={"placeholder": "Shkruaj email-in"}
        )
    )

    telefoni = forms.CharField(
        max_length=20,
        required=False,
        label="Numri i telefonit",
        widget=forms.TextInput(
            attrs={
                "placeholder": "Shkruaj numrin e telefonit",
                "type": "tel"
            }
        )
    )

    fjalekalimi = forms.CharField(
        label="Fjalëkalimi",
        strip=False,
        widget=forms.PasswordInput(
            attrs={"placeholder": "Krijo fjalëkalimin"}
        )
    )

    konfirmo_fjalekalimin = forms.CharField(
        label="Konfirmo fjalëkalimin",
        strip=False,
        widget=forms.PasswordInput(
            attrs={"placeholder": "Përsërit fjalëkalimin"}
        )
    )

    def clean_roli(self):
        return self.cleaned_data.get("roli") or "klient"

    def clean_email(self):
        email = self.cleaned_data["email"].strip().lower()
        Perdoruesi = get_user_model()

        if Perdoruesi.objects.filter(
            email__iexact=email
        ).exists():
            raise forms.ValidationError(
                "Ky email është i regjistruar tashmë."
            )

        if Perdoruesi.USERNAME_FIELD == "username":
            if len(email) > 150:
                raise forms.ValidationError(
                    "Email-i është shumë i gjatë."
                )

            if Perdoruesi.objects.filter(
                username__iexact=email
            ).exists():
                raise forms.ValidationError(
                    "Ky email është i regjistruar tashmë."
                )

            try:
                Perdoruesi._meta.get_field(
                    "username"
                ).run_validators(email)
            except ValidationError:
                raise forms.ValidationError(
                    "Email-i përmban karaktere të palejuara."
                )

        return email

    def clean(self):
        cleaned_data = super().clean()

        roli = cleaned_data.get("roli")
        telefoni = cleaned_data.get("telefoni")
        emri = cleaned_data.get("emri", "")
        mbiemri = cleaned_data.get("mbiemri", "")

        if roli == "pronar":
            if not telefoni:
                self.add_error(
                    "telefoni",
                    "Numri i telefonit është i detyrueshëm për pronarët."
                )

            if len(emri) > 100:
                self.add_error(
                    "emri",
                    "Emri nuk duhet të ketë më shumë se 100 karaktere."
                )

            if len(mbiemri) > 100:
                self.add_error(
                    "mbiemri",
                    "Mbiemri nuk duhet të ketë më shumë se 100 karaktere."
                )

        fjalekalimi = cleaned_data.get("fjalekalimi")
        konfirmimi = cleaned_data.get("konfirmo_fjalekalimin")

        if fjalekalimi and konfirmimi:
            if fjalekalimi != konfirmimi:
                self.add_error(
                    "konfirmo_fjalekalimin",
                    "Fjalëkalimet nuk përputhen."
                )
            else:
                Perdoruesi = get_user_model()

                perdoruesi = Perdoruesi(
                    username=cleaned_data.get("email", ""),
                    email=cleaned_data.get("email", ""),
                    first_name=emri,
                    last_name=mbiemri
                )

                try:
                    validate_password(
                        fjalekalimi,
                        user=perdoruesi
                    )
                except ValidationError as gabimi:
                    self.add_error(
                        "fjalekalimi",
                        gabimi
                    )

        return cleaned_data

    @transaction.atomic
    def save(self):
        Perdoruesi = get_user_model()

        email = self.cleaned_data["email"]
        roli = self.cleaned_data["roli"]

        te_dhenat = {
            "email": email,
            "first_name": self.cleaned_data["emri"],
            "last_name": self.cleaned_data["mbiemri"],
            "roli": roli,
        }

        if Perdoruesi.USERNAME_FIELD != "email":
            te_dhenat[Perdoruesi.USERNAME_FIELD] = email

        perdoruesi = Perdoruesi(**te_dhenat)

        perdoruesi.is_staff = False
        perdoruesi.is_superuser = False

        perdoruesi.set_password(
            self.cleaned_data["fjalekalimi"]
        )

        perdoruesi.full_clean()
        perdoruesi.save()

        if roli == "pronar":
            Pronari.objects.create(
                perdoruesi=perdoruesi,
                emri=self.cleaned_data["emri"],
                mbiemri=self.cleaned_data["mbiemri"],
                telefoni=self.cleaned_data["telefoni"],
                email=email
            )

        return perdoruesi