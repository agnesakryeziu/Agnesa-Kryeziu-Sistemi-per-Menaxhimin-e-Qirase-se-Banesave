from datetime import date
from decimal import Decimal

from django.core.exceptions import ValidationError
from django.test import TestCase

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
