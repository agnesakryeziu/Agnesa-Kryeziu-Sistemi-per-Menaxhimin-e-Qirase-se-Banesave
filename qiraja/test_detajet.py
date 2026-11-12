from datetime import timedelta
from decimal import Decimal

from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from .models import Banesa, Kontrata, Pronari, Qiramarresi


class TestDetajetBaneses(TestCase):
    def setUp(self):
        self.pronari = Pronari.objects.create(
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
            pronari=self.pronari
        )

        self.url = reverse(
            "detajet_baneses",
            args=[self.banesa.pk]
        )

    def test_faqja_e_detajeve_hapet(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response,
            "qiraja/detajet_baneses.html"
        )
        self.assertContains(response, "Shadervanit")
        self.assertContains(response, "Prizren")

    def test_banesa_fillimisht_eshte_e_lire(self):
        response = self.client.get(self.url)

        self.assertContains(response, "E lirë")

    def test_banesa_me_kontrate_aktive_eshte_e_zene(self):
        qiramarresi = Qiramarresi.objects.create(
            emri="Dren",
            mbiemri="Krasniqi",
            telefoni="045222333"
        )

        sot = timezone.localdate()

        Kontrata.objects.create(
            banesa=self.banesa,
            qiramarresi=qiramarresi,
            data_fillimit=sot - timedelta(days=5),
            data_mbarimit=sot + timedelta(days=30),
            qiraja_mujore=Decimal("450.00")
        )

        response = self.client.get(self.url)

        self.assertContains(response, "E zënë")

    def test_banesa_qe_nuk_ekziston_kthen_404(self):
        url = reverse(
            "detajet_baneses",
            args=[999999]
        )

        response = self.client.get(url)

        self.assertEqual(response.status_code, 404)

    def test_lidhja_e_detajeve_nga_home(self):
        response = self.client.get(reverse("home"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(
            response,
            f'href="{self.url}"'
        )

    def test_lidhja_e_detajeve_nga_banesat(self):
        response = self.client.get(reverse("banesat"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(
            response,
            f'href="{self.url}"'
        )
