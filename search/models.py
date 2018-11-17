from django.db import models

# Create your models here.
class Stock(models.Model):
    code = models.CharField(max_length=50)
    date = models.DateField()
    open_price = models.FloatField()
    high_price = models.FloatField()
    low_price = models.FloatField()
    close_price = models.FloatField()
    volume = models.IntegerField()
    objects = models.Manager()

    def __str__(self):
        return self.code