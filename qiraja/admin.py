from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import MesazhKontakti

from .models import (
    Perdorues,
    Pronari,
    Banesa,
    FotografiaBaneses,
    Qiramarresi,
    Kontrata,
    Pagesa,
)

class FotografiaBanesesInline(admin.TabularInline):
    model = FotografiaBaneses
    extra = 1
    fields = ("fotografia", "pershkrimi", "renditja")


@admin.register(Banesa)
class BanesaAdmin(admin.ModelAdmin):
    list_display = (
        "adresa",
        "qyteti",
        "siperfaqja",
        "cmimi_mujor",
        "pronari",
    )
    search_fields = ("adresa", "qyteti")
    list_filter = ("qyteti",)
    inlines = [FotografiaBanesesInline]

admin.site.register(Perdorues, UserAdmin)
admin.site.register(Pronari)
admin.site.register(Qiramarresi)
admin.site.register(Kontrata)
admin.site.register(Pagesa)

@admin.register(MesazhKontakti)
class MesazhKontaktiAdmin(admin.ModelAdmin):
    list_display = (
        "emri",
        "email",
        "subjekti",
        "krijuar_me",
    )

    search_fields = (
        "emri",
        "email",
        "subjekti",
    )

    list_filter = ("krijuar_me",)

    readonly_fields = (
        "emri",
        "email",
        "subjekti",
        "mesazhi",
        "krijuar_me",
    )

    ordering = ("-krijuar_me",)
