from datetime import timedelta
from decimal import Decimal

from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from .models import Banesa, Pronari, Qiramarresi, Kontrata


class TestFaqjaBanesat(TestCase):
    def setUp(self):
        pronari = Pronari.objects.create(
            emri="Arben",
            mbiemri="Berisha",
            telefoni="044111222"
        )

        self.banesa1 = Banesa.objects.create(
            adresa="Rruga e Shadervanit",
            qyteti="Prizren",
            siperfaqja=85,
            numri_dhomave=3,
            cmimi_mujor=Decimal("450.00"),
            pronari=pronari
        )

        self.banesa2 = Banesa.objects.create(
            adresa="Rruga e Spitalit",
            qyteti="Gjilan",
            siperfaqja=60,
            numri_dhomave=2,
            cmimi_mujor=Decimal("280.00"),
            pronari=pronari
        )

        qiramarresi = Qiramarresi.objects.create(
            emri="Dren",
            mbiemri="Krasniqi",
            telefoni="045222333"
        )

        sot = timezone.localdate()

        Kontrata.objects.create(
            banesa=self.banesa1,
            qiramarresi=qiramarresi,
            data_fillimit=sot - timedelta(days=10),
            data_mbarimit=sot + timedelta(days=30),
            qiraja_mujore=Decimal("450.00")
        )

    def test_faqja_hapet(self):
        response = self.client.get(reverse("banesat"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response,
            "qiraja/banesat.html"
        )
        self.assertEqual(
            response.context["numri_rezultateve"],
            2
        )

    def test_filtrimi_sipas_qytetit(self):
        response = self.client.get(
            reverse("banesat"),
            {"qyteti": "Prizren"}
        )

        self.assertEqual(
            response.context["numri_rezultateve"],
            1
        )
        self.assertContains(response, "Shadervanit")
        self.assertNotContains(response, "Spitalit")

    def test_kerkimi_sipas_adreses(self):
        response = self.client.get(
            reverse("banesat"),
            {"q": "Spitalit"}
        )

        self.assertEqual(
            response.context["numri_rezultateve"],
            1
        )
        self.assertContains(response, "Spitalit")

    def test_filtrimi_sipas_cmimit(self):
        response = self.client.get(
            reverse("banesat"),
            {"cmimi_max": "300"}
        )

        self.assertEqual(
            response.context["numri_rezultateve"],
            1
        )
        self.assertContains(response, "Gjilan")

    def test_filtrimi_sipas_statusit(self):
        response = self.client.get(
            reverse("banesat"),
            {"statusi": "zene"}
        )

        self.assertEqual(
            response.context["numri_rezultateve"],
            1
        )
        self.assertContains(response, "Shadervanit")

    def test_cmimi_i_pavlefshem(self):
        response = self.client.get(
            reverse("banesat"),
            {"cmimi_max": "-10"}
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.context["numri_rezultateve"],
            0
        )
        self.assertContains(
            response,
            "Çmimi maksimal nuk është i vlefshëm."
        )

    def test_renditja_sipas_cmimit(self):
        response = self.client.get(
            reverse("banesat"),
            {"renditja": "cmimi_ulte"}
        )

        banesat = list(response.context["banesat"])

        self.assertEqual(banesat[0], self.banesa2)
        self.assertEqual(banesat[1], self.banesa1)
