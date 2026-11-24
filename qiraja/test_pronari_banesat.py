from io import BytesIO
from tempfile import TemporaryDirectory

from PIL import Image
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, override_settings
from django.urls import reverse

from .models import Perdorues, Pronari, Banesa


class TestBanesatPronarit(TestCase):

    def setUp(self):
        self.user = Perdorues.objects.create_user(
            username="pronari@example.com",
            email="pronari@example.com",
            password="RentTest@2026",
            roli="pronar"
        )

        self.pronari = Pronari.objects.create(
            perdoruesi=self.user,
            emri="Arben",
            mbiemri="Krasniqi",
            telefoni="044000000",
            email="pronari@example.com"
        )

        self.pronari_tjeter = Pronari.objects.create(
            emri="Besnik",
            mbiemri="Berisha",
            telefoni="045000000",
            email="besnik@example.com"
        )

        self.banesa = Banesa.objects.create(
            adresa="Rruga e Pare",
            qyteti="Prizren",
            siperfaqja=85,
            numri_dhomave=3,
            cmimi_mujor=350,
            pronari=self.pronari
        )

        self.banesa_tjeter = Banesa.objects.create(
            adresa="Rruga e Dyte",
            qyteti="Prishtine",
            siperfaqja=100,
            numri_dhomave=4,
            cmimi_mujor=500,
            pronari=self.pronari_tjeter
        )

        self.client.force_login(self.user)

    def te_dhenat(self):
        return {
            "adresa": "Rruga e Re",
            "qyteti": "Prizren",
            "siperfaqja": 90,
            "numri_dhomave": 3,
            "cmimi_mujor": 400,
        }

    def test_hapja_e_formularit(self):
        response = self.client.get(
            reverse("pronari_shto_banese")
        )

        self.assertEqual(response.status_code, 200)

        self.assertNotIn(
            "pronari",
            response.context["form"].fields
        )

    def test_shtimi_i_baneses(self):
        response = self.client.post(
            reverse("pronari_shto_banese"),
            self.te_dhenat()
        )

        self.assertRedirects(
            response,
            reverse("paneli_pronarit")
        )

        banesa = Banesa.objects.get(
            adresa="Rruga e Re"
        )

        self.assertEqual(banesa.pronari, self.pronari)

    def test_shtimi_me_fotografi(self):
        with TemporaryDirectory() as folder:
            with override_settings(MEDIA_ROOT=folder):

                buffer = BytesIO()
                Image.new("RGB", (100, 100)).save(
                    buffer,
                    format="PNG"
                )

                te_dhenat = self.te_dhenat()

                te_dhenat["fotografia"] = SimpleUploadedFile(
                    "banesa.png",
                    buffer.getvalue(),
                    content_type="image/png"
                )

                response = self.client.post(
                    reverse("pronari_shto_banese"),
                    te_dhenat
                )

                self.assertRedirects(
                    response,
                    reverse("paneli_pronarit")
                )

                banesa = Banesa.objects.get(
                    adresa="Rruga e Re"
                )

                self.assertTrue(banesa.fotografia)

                self.assertTrue(
                    banesa.fotografia.storage.exists(
                        banesa.fotografia.name
                    )
                )

    def test_ndryshimi_i_baneses_personale(self):
        response = self.client.post(
            reverse(
                "pronari_ndrysho_banese",
                args=[self.banesa.pk]
            ),
            self.te_dhenat()
        )

        self.assertRedirects(
            response,
            reverse("paneli_pronarit")
        )

        self.banesa.refresh_from_db()

        self.assertEqual(self.banesa.adresa, "Rruga e Re")
        self.assertEqual(self.banesa.cmimi_mujor, 400)
        self.assertEqual(self.banesa.pronari, self.pronari)

    def test_ndryshimi_i_baneses_se_huaj_ndalohet(self):
        url = reverse(
            "pronari_ndrysho_banese",
            args=[self.banesa_tjeter.pk]
        )

        response = self.client.get(url)

        self.assertEqual(response.status_code, 404)

        response = self.client.post(
            url,
            self.te_dhenat()
        )

        self.assertEqual(response.status_code, 404)

        self.banesa_tjeter.refresh_from_db()

        self.assertEqual(
            self.banesa_tjeter.adresa,
            "Rruga e Dyte"
        )

    def test_nuk_mund_te_caktoje_pronar_tjeter(self):
        te_dhenat = self.te_dhenat()
        te_dhenat["pronari"] = self.pronari_tjeter.pk

        response = self.client.post(
            reverse("pronari_shto_banese"),
            te_dhenat
        )

        self.assertRedirects(
            response,
            reverse("paneli_pronarit")
        )

        banesa = Banesa.objects.get(
            adresa="Rruga e Re"
        )

        self.assertEqual(banesa.pronari, self.pronari)

    def test_te_dhenat_e_pavlefshme(self):
        te_dhenat = self.te_dhenat()

        te_dhenat["cmimi_mujor"] = -100
        te_dhenat["siperfaqja"] = 0
        te_dhenat["numri_dhomave"] = 0

        response = self.client.post(
            reverse("pronari_shto_banese"),
            te_dhenat
        )

        self.assertEqual(response.status_code, 200)

        self.assertFalse(
            Banesa.objects.filter(
                adresa="Rruga e Re"
            ).exists()
        )

    def test_klienti_nuk_mund_te_shtoje_banese(self):
        klienti = Perdorues.objects.create_user(
            username="klienti@example.com",
            email="klienti@example.com",
            password="RentTest@2026",
            roli="klient"
        )

        self.client.force_login(klienti)

        url = reverse("pronari_shto_banese")

        self.assertEqual(
            self.client.get(url).status_code,
            403
        )

        self.assertEqual(
            self.client.post(
                url,
                self.te_dhenat()
            ).status_code,
            403
        )

        self.assertFalse(
            Banesa.objects.filter(
                adresa="Rruga e Re"
            ).exists()
        )

    def test_vizitori_nuk_mund_te_shtoje_banese(self):
        self.client.logout()

        url = reverse("pronari_shto_banese")

        response = self.client.get(url)

        self.assertRedirects(
            response,
            reverse("hyrja") + "?next=" + url,
            fetch_redirect_response=False
        )