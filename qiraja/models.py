from django.db import models
from django.contrib.auth.models import AbstractUser


class Perdorues(AbstractUser):
    email = models.EmailField(unique=True)

    def _str_(self):
        return self.username