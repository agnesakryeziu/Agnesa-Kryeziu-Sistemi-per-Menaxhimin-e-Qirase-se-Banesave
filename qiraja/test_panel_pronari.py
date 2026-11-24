from django.test import TestCase
from django.urls import reverse

from .models import Perdorues, Pronari, Banesa


class TestPaneliPronarit(TestCase):

    def setUp(self):
        self.perdoruesi = Perdorues.objects.create_user(
            username="pronari1@example.com",
            email="pronari1@example.com",
            password="RentTest@2026",
            roli="pronar"
        )

        self.pronari = Pronari.objects.create(
            perdoruesi=self.perdoruesi,
            emri="Arben",
            mbiemri="Krasniqi",
            telefoni="044000000",
            email="pronari1@example.com"
        )

        self.perdoruesi_tjeter = Perdorues.objects.create_user(
            username="pronari2@example.com",
            email="pronari2@example.com",
            password="RentTest@2026",
            roli="pronar"
        )

        self.pronari_tjeter = Pronari.objects.create(
            perdoruesi=self.perdoruesi_tjeter,
            emri="Besnik",
            mbiemri="Berisha",
            telefoni="045000000",
            email="pronari2@example.com"
        )

        self.banesa = Banesa.objects.create(
            adresa="Rruga e Pronarit te Pare",
            qyteti="Prizren",
            siperfaqja=85,
            numri_dhomave=3,
            cmimi_mujor=350,
            pronari=self.pronari
        )

        self.banesa_tjeter = Banesa.objects.create(
            adresa="Rruga e Pronarit te Dyte",
            qyteti="Prishtine",
            siperfaqja=100,
            numri_dhomave=4,
            cmimi_mujor=500,
            pronari=self.pronari_tjeter
        )

    def test_pronari_hyn_ne_panel(self):
        self.client.force_login(self.perdoruesi)

        response = self.client.get(
            reverse("paneli_pronarit")
        )

        self.assertEqual(response.status_code, 200)

        self.assertTemplateUsed(
            response,
            "qiraja/panel_pronari.html"
        )

    def test_pronari_sheh_vetem_banesat_e_veta(self):
        self.client.force_login(self.perdoruesi)

        response = self.client.get(
            reverse("paneli_pronarit")
        )

        self.assertContains(
            response,
            self.banesa.adresa
        )

        self.assertNotContains(
            response,
            self.banesa_tjeter.adresa
        )

        self.assertEqual(
            response.context["numri_banesave"],
            1
        )

    def test_pronari_sheh_profilin_e_vet(self):
        self.client.force_login(self.perdoruesi)

        response = self.client.get(
            reverse("paneli_pronarit")
        )

        self.assertEqual(
            response.context["pronari"],
            self.pronari
        )

        self.assertContains(
            response,
            self.pronari.email
        )

        self.assertNotContains(
            response,
            self.pronari_tjeter.email
        )

    def test_klienti_nuk_hyn_ne_panel(self):
        klienti = Perdorues.objects.create_user(
            username="klient@example.com",
            email="klient@example.com",
            password="RentTest@2026",
            roli="klient"
        )

        self.client.force_login(klienti)

        response = self.client.get(
            reverse("paneli_pronarit")
        )

        self.assertEqual(response.status_code, 403)

    def test_vizitori_nuk_hyn_ne_panel(self):
        response = self.client.get(
            reverse("paneli_pronarit")
        )

        self.assertRedirects(
            response,
            reverse("hyrja") + "?next=" +
            reverse("paneli_pronarit"),
            fetch_redirect_response=False
        )

    def test_administratori_nuk_hyn_ne_panelin_e_pronarit(self):
        administratori = Perdorues.objects.create_user(
            username="admin@example.com",
            email="admin@example.com",
            password="RentTest@2026",
            is_staff=True
        )

        self.client.force_login(administratori)

        response = self.client.get(
            reverse("paneli_pronarit")
        )

        self.assertEqual(response.status_code, 403)

    def test_pronari_pa_profil_nuk_hyn_ne_panel(self):
        perdoruesi = Perdorues.objects.create_user(
            username="paprofil@example.com",
            email="paprofil@example.com",
            password="RentTest@2026",
            roli="pronar"
        )

        self.client.force_login(perdoruesi)

        response = self.client.get(
            reverse("paneli_pronarit")
        )

        self.assertEqual(response.status_code, 403)