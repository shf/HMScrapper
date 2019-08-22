from django.db import models
from django.contrib.auth.models import User


class Item(models.Model):
    link = models.CharField(max_length=100)
    group = models.IntegerField()
    category = models.CharField(max_length=100)
    title = models.CharField(max_length=100)
    date = models.DateTimeField(auto_now_add=True)
    regular_price = models.FloatField(null=True)
    sale_price = models.FloatField(null=True)
    discount = models.FloatField(null=True)
