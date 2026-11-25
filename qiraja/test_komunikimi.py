from django.test import TestCase
from django.urls import reverse

from .models import Perdorues, MesazhKontakti, Abonenti


class TestKomunikimi(TestCase):

    @classmethod
    def setUpTestData(cls):

        cls.admin = Perdorues.objects.create_user(
            username="admin@example.com",
            email="admin@example.com",
            is_staff=True
        )

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

        cls.mesazhi = MesazhKontakti.objects.create(
            emri="Arta Krasniqi",
            email="arta@example.com",
            subjekti="Pyetje per banese",
            mesazhi="Deshiroj me shume informacione."
        )

        cls.abonenti = Abonenti.objects.create(
            email="abonent@example.com"
        )

    def test_dergimi_i_mesazhit(self):

        response = self.client.post(
            reverse("kontaktet"),
            {
                "emri": "Dren Berisha",
                "email": "dren@example.com",
                "subjekti": "Pyetje",
                "mesazhi": "A eshte banesa e lire?"
            }
        )

        self.assertRedirects(response, reverse("kontaktet"))

        self.assertTrue(
            MesazhKontakti.objects.filter(
                email="dren@example.com",
                i_lexuar=False
            ).exists()
        )

    def test_administratori_sheh_mesazhet(self):

        self.client.force_login(self.admin)

        response = self.client.get(
            reverse("panel_mesazhet")
        )

        self.assertContains(response, self.mesazhi.mesazhi)

    def test_leximi_i_mesazhit(self):

        self.client.force_login(self.admin)

        response = self.client.post(
            reverse(
                "panel_lexo_mesazhin",
                args=[self.mesazhi.pk]
            )
        )

        self.assertRedirects(
            response,
            reverse("panel_mesazhet")
        )

        self.mesazhi.refresh_from_db()

        self.assertTrue(self.mesazhi.i_lexuar)

    def test_abonimi_i_ri(self):

        response = self.client.post(
            reverse("abonohu"),
            {"email": "test@example.com"}
        )

        self.assertEqual(response.status_code, 200)

        self.assertTrue(
            Abonenti.objects.filter(
                email="test@example.com"
            ).exists()
        )

    def test_abonimi_i_dyfishte(self):

        self.client.post(
            reverse("abonohu"),
            {"email": "abonent@example.com"}
        )

        self.client.post(
            reverse("abonohu"),
            {"email": "ABONENT@example.com"}
        )

        self.assertEqual(
            Abonenti.objects.filter(
                email="abonent@example.com"
            ).count(),
            1
        )

    def test_email_i_pavlefshem(self):

        response = self.client.post(
            reverse("abonohu"),
            {"email": "emailgabim"}
        )

        self.assertEqual(response.status_code, 400)

        self.assertFalse(
            Abonenti.objects.filter(
                email="emailgabim"
            ).exists()
        )

    def test_administratori_sheh_abonentet(self):

        self.client.force_login(self.admin)

        response = self.client.get(
            reverse("panel_abonentet")
        )

        self.assertContains(response, self.abonenti.email)

    def test_caktivizimi_i_abonentit(self):

        self.client.force_login(self.admin)

        response = self.client.post(
            reverse(
                "panel_statusi_abonentit",
                args=[self.abonenti.pk]
            )
        )

        self.assertRedirects(
            response,
            reverse("panel_abonentet")
        )

        self.abonenti.refresh_from_db()

        self.assertFalse(self.abonenti.aktiv)

    def test_riaktivizimi_i_abonentit(self):

        self.abonenti.aktiv = False
        self.abonenti.save(update_fields=["aktiv"])

        self.client.force_login(self.admin)

        self.client.post(
            reverse(
                "panel_statusi_abonentit",
                args=[self.abonenti.pk]
            )
        )

        self.abonenti.refresh_from_db()

        self.assertTrue(self.abonenti.aktiv)

    def test_ndalimi_i_qasjes_pa_autorizim(self):

        for user in [self.klienti, self.pronari]:

            self.client.force_login(user)

            for faqja in [
                "panel_mesazhet",
                "panel_abonentet"
            ]:

                with self.subTest(user=user, faqja=faqja):

                    response = self.client.get(reverse(faqja))

                    self.assertEqual(response.status_code, 403)

    def test_ndalimi_i_ndryshimeve_pa_autorizim(self):

        for user in [self.klienti, self.pronari]:

            self.client.force_login(user)

            response = self.client.post(
                reverse(
                    "panel_lexo_mesazhin",
                    args=[self.mesazhi.pk]
                )
            )

            self.assertEqual(response.status_code, 403)

            response = self.client.post(
                reverse(
                    "panel_statusi_abonentit",
                    args=[self.abonenti.pk]
                )
            )

            self.assertEqual(response.status_code, 403)

    def test_abonimi_nuk_lejohet_me_get(self):

        response = self.client.get(reverse("abonohu"))

        self.assertEqual(response.status_code, 405)

    def test_navigimi_administrativ(self):

        self.client.force_login(self.admin)

        for faqja in [
            "paneli",
            "panel_banesat",
            "panel_pronaret",
            "panel_qiramarresit",
            "panel_kontratat",
            "panel_pagesat",
            "panel_rezervimet",
            "panel_mesazhet",
            "panel_abonentet"
        ]:

            with self.subTest(faqja=faqja):

                response = self.client.get(reverse(faqja))

                self.assertEqual(response.status_code, 200)

                self.assertContains(
                    response,
                    reverse("panel_mesazhet")
                )

                self.assertContains(
                    response,
                    reverse("panel_abonentet")
                )

                self.assertContains(
                    response,
                    reverse("panel_rezervimet")
                )