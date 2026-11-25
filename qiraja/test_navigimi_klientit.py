from django.test import TestCase
from django.urls import reverse

from .models import Perdorues


class TestNavigimiKlientit(TestCase):

    @classmethod
    def setUpTestData(cls):

        cls.klienti = Perdorues.objects.create_user(
            username="klient@example.com",
            email="klient@example.com",
            roli="klient"
        )

        cls.pronari = Perdorues.objects.create_user(
            username="pronar@example.com",
            email="pronar@example.com",
            roli="pronar"
        )

        cls.admin = Perdorues.objects.create_user(
            username="admin@example.com",
            email="admin@example.com",
            is_staff=True
        )

    def test_klienti_sheh_butonin(self):

        self.client.force_login(self.klienti)

        response = self.client.get(reverse("home"))

        self.assertContains(
            response,
            reverse("klienti_rezervimet")
        )

    def test_vizitori_nuk_sheh_butonin(self):

        response = self.client.get(reverse("home"))

        self.assertNotContains(
            response,
            reverse("klienti_rezervimet")
        )

    def test_pronari_nuk_sheh_butonin(self):

        self.client.force_login(self.pronari)

        response = self.client.get(reverse("home"))

        self.assertNotContains(
            response,
            reverse("klienti_rezervimet")
        )

    def test_administratori_nuk_sheh_butonin(self):

        self.client.force_login(self.admin)

        response = self.client.get(reverse("home"))

        self.assertNotContains(
            response,
            reverse("klienti_rezervimet")
        )