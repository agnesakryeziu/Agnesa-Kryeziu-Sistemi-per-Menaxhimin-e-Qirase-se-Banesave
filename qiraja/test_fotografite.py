import tempfile
from io import BytesIO
from decimal import Decimal

from PIL import Image

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, override_settings
from django.urls import reverse

from .models import Banesa, Pronari


class TestFotografiteBanesave(TestCase):
    def setUp(self):
        self.dosja = tempfile.TemporaryDirectory()
        self.addCleanup(self.dosja.cleanup)

        self.media_settings = override_settings(
            MEDIA_ROOT=self.dosja.name
        )
        self.media_settings.enable()
        self.addCleanup(self.media_settings.disable)

        pronari = Pronari.objects.create(
            emri="Arben",
            mbiemri="Berisha",
            telefoni="044111222"
        )

        self.banesa = Banesa.objects.create(
            adresa="Rruga e Shadervanit",
            qyteti="Prizren",
            siperfaqja=85,
            numri_dhomave=3,
            cmimi_mujor=Decimal("450.00"),
            pronari=pronari
        )

    def krijo_fotografi(self):
        imazhi = Image.new(
            "RGB",
            (20, 20),
            (120, 180, 150)
        )

        buffer = BytesIO()
        imazhi.save(buffer, format="JPEG")

        return SimpleUploadedFile(
            "banesa_test.jpg",
            buffer.getvalue(),
            content_type="image/jpeg"
        )

    def ngarko_fotografine(self):
        self.banesa.fotografia.save(
            "banesa_test.jpg",
            self.krijo_fotografi(),
            save=True
        )

    def test_fotografia_ruhet(self):
        self.ngarko_fotografine()

        self.assertTrue(self.banesa.fotografia.name)
        self.assertTrue(
            self.banesa.fotografia.storage.exists(
                self.banesa.fotografia.name
            )
        )

    def test_fotografia_shfaqet_ne_home(self):
        self.ngarko_fotografine()

        response = self.client.get(reverse("home"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(
            response,
            self.banesa.fotografia.url
        )

    def test_fotografia_shfaqet_te_banesat(self):
        self.ngarko_fotografine()

        response = self.client.get(reverse("banesat"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(
            response,
            self.banesa.fotografia.url
        )

    def test_fotografia_shfaqet_te_detajet(self):
        self.ngarko_fotografine()

        response = self.client.get(
            reverse(
                "detajet_baneses",
                args=[self.banesa.pk]
            )
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(
            response,
            self.banesa.fotografia.url
        )

    def test_fotografia_ilustruese_kur_mungon(self):
        response = self.client.get(reverse("home"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(
            response,
            "/static/qiraja/img/banesa1.jpg"
        )
