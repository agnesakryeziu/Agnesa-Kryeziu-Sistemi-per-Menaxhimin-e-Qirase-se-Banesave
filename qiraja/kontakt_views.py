from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import CreateView

from .models import MesazhKontakti


class KontaktView(CreateView):
    model = MesazhKontakti
    template_name = "qiraja/kontaktet.html"
    fields = ["emri", "email", "subjekti", "mesazhi"]
    success_url = reverse_lazy("kontaktet")

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(
            self.request,
            "Mesazhi juaj u dërgua me sukses!"
        )
        return response