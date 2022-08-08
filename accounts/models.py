from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


class Group(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return(self.name)


class Subgroup(models.Model):
    name = models.CharField(max_length=100)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)

    def __str__(self):
        return(self.name)


class CustomUser(AbstractUser):
    first_name = models.CharField(max_length=254)
    last_name = models.CharField(max_length=254)
    username = models.CharField(max_length=254, unique=True)
    email = models.EmailField(max_length=254, unique=True)
    position = models.CharField(max_length=150, blank=True, default="-")
    group = models.ForeignKey(Group, on_delete=models.CASCADE, blank=True, null=True)
    subgroup = models.ForeignKey(Subgroup, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"