from django.shortcuts import render
from django.views.generic import View

from .models import Abonenti
from .abonimi_forms import AbonimiForm


class AbonohuView(View):

    http_method_names = ["post"]

    def post(self, request):

        form = AbonimiForm(request.POST)

        if not form.is_valid():

            return render(
                request,
                "qiraja/abonimi_rezultati.html",
                {
                    "sukses": False,
                    "njoftimi": "Ju lutemi shkruani një email të vlefshëm."
                },
                status=400
            )

        email = form.cleaned_data["email"]

        abonenti, krijuar = Abonenti.objects.get_or_create(
            email=email
        )

        if krijuar:

            njoftimi = "Abonimi juaj u realizua me sukses!"

        else:

            njoftimi = "Kërkesa juaj për abonim është regjistruar."

        return render(
            request,
            "qiraja/abonimi_rezultati.html",
            {
                "sukses": True,
                "njoftimi": njoftimi
            }
        )