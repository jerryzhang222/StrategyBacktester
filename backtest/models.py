from django.db import models

# Create your models here.

class DayofMovers(models.Model):
    rank = models.IntegerField()
    security = models.CharField(max_length = 250)
    price = models.FloatField()
    change_val = models.FloatField()
    change_percent = models.FloatField()
    volume = models.IntegerField()