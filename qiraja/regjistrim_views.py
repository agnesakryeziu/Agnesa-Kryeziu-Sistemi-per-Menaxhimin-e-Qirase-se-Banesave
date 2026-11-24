from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import FormView

from .regjistrim_forms import RegjistrimiForm


class RegjistrimiView(FormView):
    template_name = "qiraja/regjistrohu.html"
    form_class = RegjistrimiForm
    success_url = reverse_lazy("hyrja")
    http_method_names = ["get", "post", "head", "options"]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["regjistrimi_form"] = context["form"]
        return context

    def form_valid(self, form):
        form.save()

        messages.success(
            self.request,
            "Llogaria u krijua me sukses. "
            "Tani mund të vazhdoni me hyrjen në sistem."
        )

        return super().form_valid(form)