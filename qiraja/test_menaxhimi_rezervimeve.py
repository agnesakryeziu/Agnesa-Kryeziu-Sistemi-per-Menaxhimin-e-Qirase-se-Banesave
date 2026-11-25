from django.test import TestCase
from django.urls import reverse

from .models import Perdorues, Pronari, Banesa, Rezervimi
from .templatetags.rezervimet_status import e_padisponueshme


class TestMenaxhimiRezervimeve(TestCase):

    @classmethod
    def setUpTestData(cls):

        cls.user_pronar = Perdorues.objects.create_user(
            username="pronari@example.com",
            email="pronari@example.com",
            roli="pronar"
        )

        cls.pronari = Pronari.objects.create(
            perdoruesi=cls.user_pronar,
            emri="Arben",
            mbiemri="Krasniqi",
            telefoni="044000000"
        )

        cls.pronari_tjeter = Pronari.objects.create(
            emri="Besnik",
            mbiemri="Berisha",
            telefoni="045000000"
        )

        cls.klienti = Perdorues.objects.create_user(
            username="klienti@example.com",
            email="klienti@example.com",
            roli="klient"
        )

        cls.klienti_tjeter = Perdorues.objects.create_user(
            username="klienti2@example.com",
            email="klienti2@example.com",
            roli="klient"
        )

        cls.admin = Perdorues.objects.create_user(
            username="admin@example.com",
            email="admin@example.com",
            is_staff=True
        )

        cls.banesa = Banesa.objects.create(
            adresa="Rruga Personale",
            qyteti="Prizren",
            siperfaqja=85,
            numri_dhomave=3,
            cmimi_mujor=350,
            pronari=cls.pronari
        )

        cls.banesa_tjeter = Banesa.objects.create(
            adresa="Rruga Tjeter",
            qyteti="Gjilan",
            siperfaqja=90,
            numri_dhomave=3,
            cmimi_mujor=400,
            pronari=cls.pronari_tjeter
        )

        cls.rezervimi = Rezervimi.objects.create(
            banesa=cls.banesa,
            klienti=cls.klienti
        )

        cls.rezervimi_tjeter = Rezervimi.objects.create(
            banesa=cls.banesa_tjeter,
            klienti=cls.klienti_tjeter
        )

    def setUp(self):

        self.client.force_login(self.user_pronar)

        self.url = reverse(
            "pronari_vendimi_rezervimit",
            args=[self.rezervimi.pk]
        )

    def test_hapja_e_faqeve_te_pronarit(self):

        for faqja in [
            "pronari_banesat",
            "pronari_rezervimet",
            "pronari_kontratat",
            "pronari_pagesat",
            "pronari_profili"
        ]:

            with self.subTest(faqja=faqja):

                response = self.client.get(reverse(faqja))

                self.assertEqual(response.status_code, 200)

    def test_banesat_personale(self):

        response = self.client.get(
            reverse("pronari_banesat")
        )

        self.assertContains(response, self.banesa.adresa)
        self.assertNotContains(response, self.banesa_tjeter.adresa)

    def test_rezervimet_personale(self):

        response = self.client.get(
            reverse("pronari_rezervimet")
        )

        self.assertContains(response, self.banesa.adresa)
        self.assertNotContains(response, self.banesa_tjeter.adresa)

    def test_pranimi_i_rezervimit(self):

        response = self.client.post(
            self.url,
            {"vendimi": "prano"}
        )

        self.assertRedirects(
            response,
            reverse("pronari_rezervimet")
        )

        self.rezervimi.refresh_from_db()

        self.assertEqual(self.rezervimi.statusi, "pranuar")

    def test_refuzimi_i_rezervimit(self):

        self.client.post(
            self.url,
            {"vendimi": "refuzo"}
        )

        self.rezervimi.refresh_from_db()

        self.assertEqual(self.rezervimi.statusi, "refuzuar")

    def test_rezervimi_i_pronarit_tjeter(self):

        response = self.client.post(
            reverse(
                "pronari_vendimi_rezervimit",
                args=[self.rezervimi_tjeter.pk]
            ),
            {"vendimi": "prano"}
        )

        self.assertEqual(response.status_code, 404)

        self.rezervimi_tjeter.refresh_from_db()

        self.assertEqual(
            self.rezervimi_tjeter.statusi,
            "ne_pritje"
        )

    def test_refuzimi_automatik_i_kerkesave_te_tjera(self):

        rezervimi = Rezervimi.objects.create(
            banesa=self.banesa,
            klienti=self.klienti_tjeter
        )

        self.client.post(
            self.url,
            {"vendimi": "prano"}
        )

        rezervimi.refresh_from_db()

        self.assertEqual(rezervimi.statusi, "refuzuar")

    def test_anulimi_dhe_lirimi_i_baneses(self):

        self.client.post(
            self.url,
            {"vendimi": "prano"}
        )

        self.assertTrue(
            e_padisponueshme(
                Banesa.objects.get(pk=self.banesa.pk)
            )
        )

        self.client.post(
            self.url,
            {"vendimi": "anulo"}
        )

        self.rezervimi.refresh_from_db()

        self.assertEqual(self.rezervimi.statusi, "anuluar")

        self.assertFalse(
            e_padisponueshme(
                Banesa.objects.get(pk=self.banesa.pk)
            )
        )

    def test_klienti_sheh_vetem_rezervimet_e_veta(self):

        self.client.force_login(self.klienti)

        response = self.client.get(
            reverse("klienti_rezervimet")
        )

        self.assertContains(response, self.banesa.adresa)
        self.assertNotContains(response, self.banesa_tjeter.adresa)

    def test_administratori_sheh_te_gjitha_rezervimet(self):

        self.client.force_login(self.admin)

        response = self.client.get(
            reverse("panel_rezervimet")
        )

        self.assertContains(response, self.banesa.adresa)
        self.assertContains(response, self.banesa_tjeter.adresa)

    def test_ndalimi_i_qasjes_se_klientit(self):

        self.client.force_login(self.klienti)

        for faqja in [
            "pronari_banesat",
            "pronari_rezervimet",
            "pronari_kontratat",
            "pronari_pagesat",
            "pronari_profili",
            "panel_rezervimet"
        ]:

            with self.subTest(faqja=faqja):

                response = self.client.get(reverse(faqja))

                self.assertEqual(response.status_code, 403)

    def test_vendimi_vetem_nga_pronari(self):

        for user in [self.klienti, self.admin]:

            with self.subTest(user=user):

                self.client.force_login(user)

                response = self.client.post(
                    self.url,
                    {"vendimi": "prano"}
                )

                self.assertEqual(response.status_code, 403)

        self.rezervimi.refresh_from_db()

        self.assertEqual(self.rezervimi.statusi, "ne_pritje")

    def test_vendimi_nuk_lejohet_me_get(self):

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 405)