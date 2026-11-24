from django.test import TestCase
from django.urls import reverse

from .models import Perdorues, Pronari


class TestRolet(TestCase):

    def te_dhenat(self, roli="klient"):
        return {
            "roli": roli,
            "emri": "Arben",
            "mbiemri": "Krasniqi",
            "email": "test@example.com",
            "telefoni": "044000000",
            "fjalekalimi": "RentTest@2026",
            "konfirmo_fjalekalimin": "RentTest@2026",
        }

    def test_regjistrimi_klientit(self):
        response = self.client.post(
            reverse("regjistrohu"),
            self.te_dhenat()
        )

        self.assertRedirects(response, reverse("hyrja"))

        perdoruesi = Perdorues.objects.get(
            email="test@example.com"
        )

        self.assertEqual(perdoruesi.roli, "klient")
        self.assertFalse(perdoruesi.is_staff)
        self.assertFalse(perdoruesi.is_superuser)
        self.assertTrue(
            perdoruesi.check_password("RentTest@2026")
        )
        self.assertFalse(
            Pronari.objects.filter(
                perdoruesi=perdoruesi
            ).exists()
        )

    def test_regjistrimi_pronarit(self):
        response = self.client.post(
            reverse("regjistrohu"),
            self.te_dhenat("pronar")
        )

        self.assertRedirects(response, reverse("hyrja"))

        perdoruesi = Perdorues.objects.get(
            email="test@example.com"
        )

        self.assertEqual(perdoruesi.roli, "pronar")
        self.assertFalse(perdoruesi.is_staff)
        self.assertFalse(perdoruesi.is_superuser)

        pronari = Pronari.objects.get(
            perdoruesi=perdoruesi
        )

        self.assertEqual(pronari.emri, "Arben")
        self.assertEqual(pronari.telefoni, "044000000")

    def test_pronari_pa_telefon(self):
        te_dhenat = self.te_dhenat("pronar")
        te_dhenat["telefoni"] = ""

        response = self.client.post(
            reverse("regjistrohu"),
            te_dhenat
        )

        self.assertEqual(response.status_code, 200)

        self.assertFalse(
            Perdorues.objects.filter(
                email="test@example.com"
            ).exists()
        )

    def test_regjistrimi_si_administrator_ndalohet(self):
        response = self.client.post(
            reverse("regjistrohu"),
            self.te_dhenat("administrator")
        )

        self.assertEqual(response.status_code, 200)

        self.assertFalse(
            Perdorues.objects.filter(
                email="test@example.com"
            ).exists()
        )

    def test_hyrja_sipas_roleve(self):
        for roli, is_staff, faqja in [
            ("klient", False, "home"),
            ("pronar", False, "home"),
            ("klient", True, "paneli"),
        ]:
            with self.subTest(roli=roli, is_staff=is_staff):
                email = f"{roli}-{is_staff}@example.com"

                Perdorues.objects.create_user(
                    username=email,
                    email=email,
                    password="RentTest@2026",
                    roli=roli,
                    is_staff=is_staff
                )

                response = self.client.post(
                    reverse("hyrja"),
                    {
                        "username": email,
                        "password": "RentTest@2026",
                    }
                )

                self.assertRedirects(
                    response,
                    reverse(faqja),
                    fetch_redirect_response=False
                )

                self.client.logout()

    def test_qasja_administrative_ndalohet(self):
        for roli in ["klient", "pronar"]:
            with self.subTest(roli=roli):
                perdoruesi = Perdorues.objects.create_user(
                    username=f"{roli}@example.com",
                    email=f"{roli}@example.com",
                    password="RentTest@2026",
                    roli=roli
                )

                self.client.force_login(perdoruesi)

                response = self.client.get(
                    reverse("paneli")
                )

                self.assertEqual(response.status_code, 403)

                response_api = self.client.get(
                    "/api/pronaret/"
                )

                self.assertEqual(
                    response_api.status_code,
                    403
                )

                self.client.logout()