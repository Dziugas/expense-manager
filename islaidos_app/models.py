from django.db import models

class Islaidu_tipai(models.Model):
    tipas = models.CharField(max_length=50)
    aktyvus = models.BooleanField()

    def __str__(self):
        return self.tipas

class Islaidos(models.Model):
    data = models.DateTimeField()
    tiekejas = models.CharField(max_length=100)
    tipas = models.ForeignKey(Islaidu_tipai, on_delete=models.CASCADE)
    dok_nr = models.IntegerField()
    suma = models.DecimalField(max_digits=9, decimal_places=2)

    def __str__(self):
        return self.tipas


