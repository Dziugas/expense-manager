from django.db import models

class Islaidos(models.Model):
    data = models.DateTimeField()
    tipas = models.CharField(max_length=100)
    tiekejas = models.CharField(max_length=50)
    dok_nr = models.IntegerField()
    suma = models.DecimalField(max_digits=9, decimal_places=2)


    def __str__(self):
        return self.tipas


