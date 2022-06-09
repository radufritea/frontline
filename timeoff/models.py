from django.db import models
from accounts.models import CustomUser

# Create your models here.
class TypeOfTimeoff(models.Model):
    models.CharField(max_length=254)

class TimeoffRequest(models.Model):
    employee = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    comment = models.TextField(blank=True)
    approved_N1 = models.BooleanField(default=False)
    approved_N2 = models.BooleanField(default=False)