from datetime import timedelta

from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from .models import (
    Perdorues,
    Pronari,
    Banesa,
    Qiramarresi,
    Kontrata,
    Pagesa,
)


class TestPronariFinancat(TestCase):

    @classmethod
    def setUpTestData(cls):

        cls.user = Perdorues.objects.create_user(
            username="pronari@example.com",
            email="pronari@example.com",
            roli="pronar"
        )

        cls.admin = Perdorues.objects.create_user(
            username="admin@example.com",
            email="admin@example.com",
            is_staff=True
        )

        cls.pronari = Pronari.objects.create(
            perdoruesi=cls.user,
            emri="Arben",
            mbiemri="Krasniqi",
            telefoni="044000000",
            email="pronari@example.com"
        )

        cls.pronari_tjeter = Pronari.objects.create(
            emri="Besnik",
            mbiemri="Berisha",
            telefoni="045000000",
            email="besnik@example.com"
        )

        cls.banesa = Banesa.objects.create(
            adresa="Banesa Personale",
            qyteti="Prizren",
            siperfaqja=85,
            numri_dhomave=3,
            cmimi_mujor=350,
            pronari=cls.pronari,
            fotografia="banesat/banesa-personale.jpg"
        )

        cls.banesa_tjeter = Banesa.objects.create(
            adresa="Banesa e Pronarit Tjeter",
            qyteti="Gjilan",
            siperfaqja=100,
            numri_dhomave=4,
            cmimi_mujor=500,
            pronari=cls.pronari_tjeter,
            fotografia="banesat/banesa-tjeter.jpg"
        )

        cls.qiramarresi = Qiramarresi.objects.create(
            emri="Dren",
            mbiemri="Gashi",
            telefoni="049000000",
            email="dren@example.com"
        )

        sot = timezone.localdate()

        cls.kontrata = Kontrata.objects.create(
            banesa=cls.banesa,
            qiramarresi=cls.qiramarresi,
            data_fillimit=sot - timedelta(days=10),
            data_mbarimit=sot + timedelta(days=90),
            qiraja_mujore=350,
            status="aktive"
        )

        cls.kontrata_tjeter = Kontrata.objects.create(
            banesa=cls.banesa_tjeter,
            qiramarresi=cls.qiramarresi,
            data_fillimit=sot - timedelta(days=10),
            data_mbarimit=sot + timedelta(days=90),
            qiraja_mujore=500,
            status="aktive"
        )

        cls.pagesa = Pagesa.objects.create(
            kontrata=cls.kontrata,
            data_pageses=sot,
            shuma=350,
            muaji=sot.month,
            viti=sot.year,
            e_paguar=True
        )

        cls.pagesa_tjeter = Pagesa.objects.create(
            kontrata=cls.kontrata_tjeter,
            data_pageses=sot,
            shuma=500,
            muaji=sot.month,
            viti=sot.year,
            e_paguar=False
        )

    def test_kontratat_personale(self):

        self.client.force_login(self.user)

        response = self.client.get(
            reverse("pronari_kontratat")
        )

        self.assertEqual(response.status_code, 200)

        self.assertContains(
            response,
            self.banesa.adresa
        )

        self.assertNotContains(
            response,
            self.banesa_tjeter.adresa
        )

        self.assertContains(
            response,
            self.banesa.fotografia.url
        )

        self.assertNotContains(
            response,
            self.banesa_tjeter.fotografia.url
        )

    def test_pagesat_personale(self):

        self.client.force_login(self.user)

        response = self.client.get(
            reverse("pronari_pagesat")
        )

        self.assertEqual(response.status_code, 200)

        self.assertContains(
            response,
            self.banesa.adresa
        )

        self.assertNotContains(
            response,
            self.banesa_tjeter.adresa
        )

        self.assertContains(
            response,
            self.banesa.fotografia.url
        )

        self.assertNotContains(
            response,
            self.banesa_tjeter.fotografia.url
        )

    def test_administratori_sheh_kontratat(self):

        self.client.force_login(self.admin)

        response = self.client.get(
            reverse("panel_kontratat")
        )

        self.assertEqual(response.status_code, 200)

        self.assertContains(
            response,
            self.banesa.fotografia.url
        )

        self.assertContains(
            response,
            self.banesa_tjeter.fotografia.url
        )

    def test_administratori_sheh_pagesat(self):

        self.client.force_login(self.admin)

        response = self.client.get(
            reverse("panel_pagesat")
        )

        self.assertEqual(response.status_code, 200)

        self.assertContains(
            response,
            self.banesa.fotografia.url
        )

        self.assertContains(
            response,
            self.banesa_tjeter.fotografia.url
        )

    def test_pronari_nuk_hyn_ne_financat_administrative(self):

        self.client.force_login(self.user)

        for faqja in ["panel_kontratat", "panel_pagesat"]:

            with self.subTest(faqja=faqja):

                response = self.client.get(
                    reverse(faqja)
                )

                self.assertEqual(response.status_code, 403)