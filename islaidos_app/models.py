from django.db import models
from datetime import datetime
from django.contrib.auth.models import User

class Keeper(models.Model):
    keeper_name = models.CharField(max_length=50, default=None)
    date = models.DateTimeField(blank=True, default=datetime.now)
    users = models.ManyToManyField(User, related_name='keepers', default=None)

class ExpenseTypes(models.Model):
    tipas = models.CharField(max_length=50)
    aktyvus = models.BooleanField(default=False)
    keeper = models.ForeignKey(Keeper, default=None, on_delete=models.CASCADE)

    def __str__(self):
        return self.tipas

class Expenses(models.Model):
    data = models.DateTimeField()
    tiekejas = models.CharField(max_length=100)
    description = models.CharField(max_length=100)
    tipas = models.ForeignKey(ExpenseTypes, on_delete=models.CASCADE)
    dok_nr = models.IntegerField()
    suma = models.DecimalField(max_digits=9, decimal_places=2)
    keeper = models.ForeignKey(Keeper, default=None, on_delete=models.CASCADE)

    def __str__(self):
        return self.tiekejas


