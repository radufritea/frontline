from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    first_name = models.CharField(max_length=254)
    last_name = models.CharField(max_length=254)
    username = models.CharField(max_length=254, unique=True)
    email = models.EmailField(max_length=254, unique=True)
    position = models.CharField(max_length=150, blank=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"