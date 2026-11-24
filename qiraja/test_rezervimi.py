from datetime import timedelta

from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from .models import (
    Perdorues,
    Pronari,
    Banesa,
    Rezervimi,
    Qiramarresi,
    Kontrata,
)


class TestRezervimi(TestCase):

    @classmethod
    def setUpTestData(cls):

        cls.klienti = Perdorues.objects.create_user(
            username="klienti@example.com",
            email="klienti@example.com",
            password="RentTest@2026",
            roli="klient"
        )

        cls.perdoruesi_pronar = Perdorues.objects.create_user(
            username="pronari@example.com",
            email="pronari@example.com",
            password="RentTest@2026",
            roli="pronar"
        )

        cls.pronari = Pronari.objects.create(
            perdoruesi=cls.perdoruesi_pronar,
            emri="Arben",
            mbiemri="Krasniqi",
            telefoni="044000000",
            email="pronari@example.com"
        )

        cls.banesa = Banesa.objects.create(
            adresa="Rruga e Spitalit",
            qyteti="Gjilan",
            siperfaqja=65,
            numri_dhomave=2,
            cmimi_mujor=480,
            pronari=cls.pronari
        )

    def setUp(self):

        self.url = reverse(
            "rezervo_banese",
            args=[self.banesa.pk]
        )

        self.client.force_login(self.klienti)

    def test_hapja_e_formularit(self):

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)

        self.assertTemplateUsed(
            response,
            "qiraja/rezervo_banese.html"
        )

    def test_krijimi_i_rezervimit(self):

        response = self.client.post(
            self.url,
            {"mesazhi": "Jam i interesuar per banesen."}
        )

        self.assertRedirects(
            response,
            reverse("home")
        )

        rezervimi = Rezervimi.objects.get(
            banesa=self.banesa,
            klienti=self.klienti
        )

        self.assertEqual(
            rezervimi.statusi,
            "ne_pritje"
        )

    def test_rezervimi_i_dyfishte_ndalohet(self):

        Rezervimi.objects.create(
            banesa=self.banesa,
            klienti=self.klienti
        )

        response = self.client.post(
            self.url,
            {"mesazhi": "Kerkese tjeter"}
        )

        self.assertEqual(response.status_code, 200)

        self.assertEqual(
            Rezervimi.objects.filter(
                banesa=self.banesa,
                klienti=self.klienti
            ).count(),
            1
        )

    def test_pronari_nuk_mund_te_rezervoje(self):

        self.client.force_login(
            self.perdoruesi_pronar
        )

        response = self.client.post(
            self.url,
            {"mesazhi": "Rezervim"}
        )

        self.assertEqual(response.status_code, 403)
        self.assertEqual(Rezervimi.objects.count(), 0)

    def test_administratori_nuk_mund_te_rezervoje(self):

        administratori = Perdorues.objects.create_user(
            username="admin@example.com",
            email="admin@example.com",
            password="RentTest@2026",
            is_staff=True
        )

        self.client.force_login(administratori)

        response = self.client.post(
            self.url,
            {"mesazhi": "Rezervim"}
        )

        self.assertEqual(response.status_code, 403)
        self.assertEqual(Rezervimi.objects.count(), 0)

    def test_vizitori_duhet_te_kycet(self):

        self.client.logout()

        response = self.client.get(self.url)

        self.assertRedirects(
            response,
            reverse("hyrja") + "?next=" + self.url,
            fetch_redirect_response=False
        )

    def test_ridrejtimi_pas_kycjes(self):

        self.client.logout()

        response = self.client.post(
            reverse("hyrja"),
            {
                "username": "klienti@example.com",
                "password": "RentTest@2026",
                "next": self.url,
            }
        )

        self.assertRedirects(response, self.url)

    def test_ruajtja_e_adreses_ne_formularin_e_hyrjes(self):

        self.client.logout()

        response = self.client.get(
            reverse("hyrja"),
            {"next": self.url}
        )

        self.assertContains(response, 'name="next"')
        self.assertContains(response, self.url)

    def test_banesa_e_zene_nuk_rezervohet(self):

        qiramarresi = Qiramarresi.objects.create(
            emri="Besnik",
            mbiemri="Berisha",
            telefoni="045000000",
            email="besnik@example.com"
        )

        sot = timezone.localdate()

        Kontrata.objects.create(
            banesa=self.banesa,
            qiramarresi=qiramarresi,
            data_fillimit=sot - timedelta(days=5),
            data_mbarimit=sot + timedelta(days=30),
            qiraja_mujore=480,
            status="aktive"
        )

        response = self.client.post(
            self.url,
            {"mesazhi": "Rezervim"}
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(Rezervimi.objects.count(), 0)

    def test_banesa_me_rezervim_te_pranuar(self):

        klienti_tjeter = Perdorues.objects.create_user(
            username="klienti2@example.com",
            email="klienti2@example.com",
            password="RentTest@2026",
            roli="klient"
        )

        Rezervimi.objects.create(
            banesa=self.banesa,
            klienti=klienti_tjeter,
            statusi="pranuar"
        )

        response = self.client.post(
            self.url,
            {"mesazhi": "Rezervim"}
        )

        self.assertEqual(response.status_code, 200)

        self.assertFalse(
            Rezervimi.objects.filter(
                klienti=self.klienti
            ).exists()
        )

    def test_mesazhi_shume_i_gjate(self):

        response = self.client.post(
            self.url,
            {"mesazhi": "a" * 1001}
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(Rezervimi.objects.count(), 0)