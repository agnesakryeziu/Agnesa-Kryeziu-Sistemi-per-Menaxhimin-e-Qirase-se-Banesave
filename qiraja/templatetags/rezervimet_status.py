from django import template
from django.utils import timezone

from qiraja.models import Banesa, Kontrata, Rezervimi


register = template.Library()


@register.filter
def e_padisponueshme(banesa):

    if not isinstance(banesa, Banesa):
        return False

    if hasattr(banesa, "_statusi_rezervimit"):
        return banesa._statusi_rezervimit

    sot = timezone.localdate()

    ka_kontrate = Kontrata.objects.filter(
        banesa=banesa,
        status="aktive",
        data_fillimit__lte=sot,
        data_mbarimit__gte=sot
    ).exists()

    ka_rezervim = Rezervimi.objects.filter(
        banesa=banesa,
        statusi="pranuar"
    ).exists()

    banesa._statusi_rezervimit = ka_kontrate or ka_rezervim

    return banesa._statusi_rezervimit