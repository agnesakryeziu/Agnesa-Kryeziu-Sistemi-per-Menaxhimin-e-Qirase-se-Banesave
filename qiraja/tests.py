from datetime import date
from decimal import Decimal

from django.core.exceptions import ValidationError
from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from rest_framework import status

from .models import Pronari, Banesa, Qiramarresi, Kontrata, Pagesa


class TestValidimet(TestCase):

    def setUp(self):
        self.pronari = Pronari.objects.create(
            emri="Arianita",
            mbiemri="Gashi",
            telefoni="044000111"
        )

        self.banesa = Banesa.objects.create(
            adresa="Rruga B, Nr. 12",
            qyteti="Prishtine",
            siperfaqja=75,
            numri_dhomave=3,
            cmimi_mujor=Decimal("350.00"),
            pronari=self.pronari
        )

        self.qiramarresi = Qiramarresi.objects.create(
            emri="Dren",
            mbiemri="Berisha",
            telefoni="045000222"
        )

        self.kontrata = Kontrata.objects.create(
            banesa=self.banesa,
            qiramarresi=self.qiramarresi,
            data_fillimit=date(2026, 11, 1),
            data_mbarimit=date(2027, 10, 31),
            qiraja_mujore=Decimal("350.00")
        )

    def test_kontrata_me_data_te_gabuara(self):
        kontrata = Kontrata(
            banesa=self.banesa,
            qiramarresi=self.qiramarresi,
            data_fillimit=date(2027, 5, 1),
            data_mbarimit=date(2027, 4, 1),
            qiraja_mujore=Decimal("350.00")
        )

        with self.assertRaises(ValidationError):
            kontrata.full_clean()

    def test_kontrata_me_periudhe_te_mbivendosur(self):
        kontrata = Kontrata(
            banesa=self.banesa,
            qiramarresi=self.qiramarresi,
            data_fillimit=date(2027, 1, 1),
            data_mbarimit=date(2027, 12, 31),
            qiraja_mujore=Decimal("350.00")
        )

        with self.assertRaises(ValidationError):
            kontrata.full_clean()

    def test_pagesa_me_muaj_te_pavlefshem(self):
        pagesa = Pagesa(
            kontrata=self.kontrata,
            data_pageses=date(2026, 11, 5),
            shuma=Decimal("350.00"),
            muaji=13,
            viti=2026,
            e_paguar=True
        )

        with self.assertRaises(ValidationError):
            pagesa.full_clean()

    def test_pagesa_e_dyfishte(self):
        Pagesa.objects.create(
            kontrata=self.kontrata,
            data_pageses=date(2026, 11, 5),
            shuma=Decimal("350.00"),
            muaji=11,
            viti=2026,
            e_paguar=True
        )

        pagesa_tjeter = Pagesa(
            kontrata=self.kontrata,
            data_pageses=date(2026, 11, 10),
            shuma=Decimal("350.00"),
            muaji=11,
            viti=2026,
            e_paguar=True
        )

        with self.assertRaises(ValidationError):
            pagesa_tjeter.full_clean()

class TestAPIPronaret(APITestCase):

    def setUp(self):
        User = get_user_model()

        self.admin = User.objects.create_superuser(
            username="admin_test",
            email="admin_test@example.com",
            password="TestPassword123!"
        )

        self.perdorues = User.objects.create_user(
            username="perdorues_test",
            email="perdorues_test@example.com",
            password="TestPassword123!"
        )

    def test_get_pa_autentikim(self):
        response = self.client.get("/api/pronaret/")
        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN
        )

    def test_get_me_admin(self):
        self.client.force_authenticate(user=self.admin)

        response = self.client.get("/api/pronaret/")

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

    def test_get_me_perdorues_pa_leje(self):
        self.client.force_authenticate(user=self.perdorues)

        response = self.client.get("/api/pronaret/")

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN
        )

    def test_post_pronar(self):
        self.client.force_authenticate(user=self.admin)

        te_dhenat = {
            "emri": "Besnik",
            "mbiemri": "Berisha",
            "telefoni": "045000333",
            "email": "besnik_test@example.com"
        }

        response = self.client.post(
            "/api/pronaret/",
            te_dhenat,
            format="json"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )

    def test_post_me_emër_bosh(self):
        self.client.force_authenticate(user=self.admin)

        te_dhenat = {
            "emri": "",
            "mbiemri": "Berisha",
            "telefoni": "045000333",
            "email": "besnik_test@example.com"
        }

        response = self.client.post(
            "/api/pronaret/",
            te_dhenat,
            format="json"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )

    def test_get_id_qe_nuk_ekziston(self):
        self.client.force_authenticate(user=self.admin)

        response = self.client.get("/api/pronaret/999999/")

        self.assertEqual(
            response.status_code,
            status.HTTP_404_NOT_FOUND        )

class TestAPIModulet(APITestCase):

    def setUp(self):
        User = get_user_model()

        self.admin = User.objects.create_superuser(
            username="admin_modulet",
            email="admin_modulet@example.com",
            password="TestPassword123!"
        )

        self.client.force_authenticate(user=self.admin)

        self.pronari = Pronari.objects.create(
            emri="Arianita",
            mbiemri="Gashi",
            telefoni="044000111"
        )

        self.banesa = Banesa.objects.create(
            adresa="Rruga A, Nr. 10",
            qyteti="Prishtine",
            siperfaqja=75,
            numri_dhomave=3,
            cmimi_mujor=Decimal("350.00"),
            pronari=self.pronari
        )

        self.qiramarresi = Qiramarresi.objects.create(
            emri="Dren",
            mbiemri="Berisha",
            telefoni="045000222"
        )

    def test_crud_banesat(self):
        te_dhenat = {
            "adresa": "Rruga B, Nr. 20",
            "qyteti": "Prishtine",
            "siperfaqja": 80,
            "numri_dhomave": 3,
            "cmimi_mujor": "400.00",
            "pronari": self.pronari.id
        }

        response = self.client.post(
            "/api/banesat/", te_dhenat, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        banesa_id = response.data["id"]
        url = f"/api/banesat/{banesa_id}/"

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.patch(
            url, {"cmimi_mujor": "450.00"}, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_crud_qiramarresit(self):
        te_dhenat = {
            "emri": "Ardit",
            "mbiemri": "Krasniqi",
            "telefoni": "049000333",
            "email": "ardit@example.com"
        }

        response = self.client.post(
            "/api/qiramarresit/", te_dhenat, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        qiramarresi_id = response.data["id"]
        url = f"/api/qiramarresit/{qiramarresi_id}/"

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.patch(
            url, {"telefoni": "049000444"}, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_crud_kontratat(self):
        te_dhenat = {
            "banesa": self.banesa.id,
            "qiramarresi": self.qiramarresi.id,
            "data_fillimit": "2026-11-01",
            "data_mbarimit": "2027-10-31",
            "qiraja_mujore": "350.00"
        }

        response = self.client.post(
            "/api/kontratat/", te_dhenat, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        kontrata_id = response.data["id"]
        url = f"/api/kontratat/{kontrata_id}/"

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.patch(
            url, {"qiraja_mujore": "370.00"}, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_crud_pagesat(self):
        kontrata = Kontrata.objects.create(
            banesa=self.banesa,
            qiramarresi=self.qiramarresi,
            data_fillimit=date(2026, 11, 1),
            data_mbarimit=date(2027, 10, 31),
            qiraja_mujore=Decimal("350.00")
        )

        te_dhenat = {
            "kontrata": kontrata.id,
            "data_pageses": "2026-11-05",
            "shuma": "350.00",
            "muaji": 11,
            "viti": 2026,
            "e_paguar": True
        }

        response = self.client.post(
            "/api/pagesat/", te_dhenat, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        pagesa_id = response.data["id"]
        url = f"/api/pagesat/{pagesa_id}/"

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.patch(
            url, {"e_paguar": False}, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)