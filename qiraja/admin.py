from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import (
    Perdorues,
    Pronari,
    Banesa,
    Qiramarresi,
    Kontrata,
    Pagesa,
)

admin.site.register(Perdorues, UserAdmin)
admin.site.register(Pronari)
admin.site.register(Banesa)
admin.site.register(Qiramarresi)
admin.site.register(Kontrata)
admin.site.register(Pagesa)