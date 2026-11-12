import tempfile
from io import BytesIO
from decimal import Decimal

from PIL import Image

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, override_settings
from django.urls import reverse

from .models import Banesa, FotografiaBaneses, Pronari


class TestGaleriaBanesave(TestCase):
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

        self.banesa_tjeter = Banesa.objects.create(
            adresa="Rruga e Spitalit",
            qyteti="Gjilan",
            siperfaqja=60,
            numri_dhomave=2,
            cmimi_mujor=Decimal("280.00"),
            pronari=pronari
        )

    def krijo_imazh(self, emri):
        imazhi = Image.new(
            "RGB",
            (30, 30),
            (140, 170, 150)
        )

        buffer = BytesIO()
        imazhi.save(buffer, format="JPEG")

        return SimpleUploadedFile(
            emri,
            buffer.getvalue(),
            content_type="image/jpeg"
        )

    def shto_fotografi(self, banesa, emri, pershkrimi, renditja):
        return FotografiaBaneses.objects.create(
            banesa=banesa,
            fotografia=self.krijo_imazh(emri),
            pershkrimi=pershkrimi,
            renditja=renditja
        )

    def test_nje_banese_ka_shume_fotografi(self):
        self.shto_fotografi(
            self.banesa, "sallon.jpg", "Salloni", 1
        )
        self.shto_fotografi(
            self.banesa, "banjo.jpg", "Banjo", 2
        )

        self.assertEqual(
            self.banesa.fotografite.count(),
            2
        )

    def test_fotografite_shfaqen_te_detajet(self):
        foto1 = self.shto_fotografi(
            self.banesa, "sallon.jpg", "Salloni", 1
        )

        foto2 = self.shto_fotografi(
            self.banesa, "banjo.jpg", "Banjo", 2
        )

        response = self.client.get(
            reverse(
                "detajet_baneses",
                args=[self.banesa.pk]
            )
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, foto1.fotografia.url)
        self.assertContains(response, foto2.fotografia.url)
        self.assertContains(response, "Salloni")
        self.assertContains(response, "Banjo")

    def test_fotografite_nuk_perzihen(self):
        foto1 = self.shto_fotografi(
            self.banesa, "sallon.jpg", "Salloni", 1
        )

        foto2 = self.shto_fotografi(
            self.banesa_tjeter,
            "kuzhine.jpg",
            "Kuzhina",
            1
        )

        response = self.client.get(
            reverse(
                "detajet_baneses",
                args=[self.banesa.pk]
            )
        )

        self.assertContains(response, foto1.fotografia.url)
        self.assertNotContains(response, foto2.fotografia.url)

    def test_renditja_e_fotografive(self):
        foto2 = self.shto_fotografi(
            self.banesa, "banjo.jpg", "Banjo", 2
        )

        foto1 = self.shto_fotografi(
            self.banesa, "sallon.jpg", "Salloni", 1
        )

        fotografite = list(self.banesa.fotografite.all())

        self.assertEqual(fotografite[0], foto1)
        self.assertEqual(fotografite[1], foto2)

    def test_banesa_pa_galeri_shfaq_fotografi_ilustruese(self):
        response = self.client.get(
            reverse(
                "detajet_baneses",
                args=[self.banesa.pk]
            )
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Fotografi ilustruese")
        self.assertContains(
            response,
            "/static/qiraja/img/banesa1.jpg"
        )
