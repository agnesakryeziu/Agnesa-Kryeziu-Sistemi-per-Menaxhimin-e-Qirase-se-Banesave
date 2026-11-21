from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy


class HyrjeView(LoginView):
    template_name = "qiraja/hyrja.html"
    next_page = reverse_lazy("paneli")

    def form_valid(self, form):
        perdoruesi = form.get_user()

        if not perdoruesi.is_staff:
            form.add_error(
                None,
                "Kjo faqe është vetëm për administratorin."
            )
            return self.form_invalid(form)

        return super().form_valid(form)


class DaljeView(LogoutView):
    next_page = reverse_lazy("home")