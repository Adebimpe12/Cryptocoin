from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class MakePayment(models.Model):
    payment_id = models.AutoField(primary_key=True)
    payment_date = models.DateTimeField(auto_now_add=True, unique=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, unique=False)
    amount = models.IntegerField(unique=False)