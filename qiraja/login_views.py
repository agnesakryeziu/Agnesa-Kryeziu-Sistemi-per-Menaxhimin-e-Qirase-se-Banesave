from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy


class HyrjeView(LoginView):
    template_name = "qiraja/hyrja.html"

    def get_success_url(self):
        perdoruesi = self.request.user

        if perdoruesi.is_staff:
            return reverse_lazy("paneli")

        return reverse_lazy("home")


class DaljeView(LogoutView):
    next_page = reverse_lazy("home")