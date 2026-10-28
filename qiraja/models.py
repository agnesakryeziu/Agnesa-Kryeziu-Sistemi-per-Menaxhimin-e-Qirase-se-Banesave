from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError


class Perdorues(AbstractUser):
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.username


class Pronari(models.Model):
    emri = models.CharField(max_length=100)
    mbiemri = models.CharField(max_length=100)
    telefoni = models.CharField(max_length=20)
    email = models.EmailField(blank=True)

    def __str__(self):
        return f"{self.emri} {self.mbiemri}"


class Banesa(models.Model):
    adresa = models.CharField(max_length=200)
    qyteti = models.CharField(max_length=100)
    siperfaqja = models.PositiveIntegerField()
    numri_dhomave = models.PositiveIntegerField()
    cmimi_mujor = models.DecimalField(max_digits=10, decimal_places=2)

    pronari = models.ForeignKey(
        Pronari,
        on_delete=models.PROTECT,
        related_name='banesat'
    )

    def __str__(self):
        return f"{self.adresa} - {self.qyteti}"


class Qiramarresi(models.Model):
    emri = models.CharField(max_length=100)
    mbiemri = models.CharField(max_length=100)
    telefoni = models.CharField(max_length=20)
    email = models.EmailField(blank=True)

    def __str__(self):
        return f"{self.emri} {self.mbiemri}"


class Kontrata(models.Model):
    banesa = models.ForeignKey(
        Banesa,
        on_delete=models.PROTECT,
        related_name='kontratat'
    )
    qiramarresi = models.ForeignKey(
        Qiramarresi,
        on_delete=models.PROTECT,
        related_name='kontratat'
    )
    data_fillimit = models.DateField()
    data_mbarimit = models.DateField()
    qiraja_mujore = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    def clean(self):
        if self.data_fillimit and self.data_mbarimit:
            if self.data_mbarimit <= self.data_fillimit:
                raise ValidationError(
                    "Data e mbarimit duhet te jete pas dates se fillimit."
                )

    def __str__(self):
        return f"Kontrata {self.id} - {self.banesa}"


class Pagesa(models.Model):
    kontrata = models.ForeignKey(
        Kontrata,
        on_delete=models.PROTECT,
        related_name='pagesat'
    )
    data_pageses = models.DateField()
    shuma = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )
    muaji = models.PositiveSmallIntegerField()
    viti = models.PositiveIntegerField()
    e_paguar = models.BooleanField(default=False)

    def clean(self):
        if self.muaji is not None and not 1 <= self.muaji <= 12:
            raise ValidationError(
                "Muaji duhet te jete nga 1 deri ne 12."
            )

        if self.shuma is not None and self.shuma <= 0:
            raise ValidationError(
                "Shuma e pageses duhet te jete me e madhe se zero."
            )

    def __str__(self):
        return f"Pagesa {self.muaji}/{self.viti} - Kontrata {self.kontrata_id}"
