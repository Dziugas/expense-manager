from django.contrib import admin
from . models import Expenses, ExpenseTypes, Keeper

admin.site.register(Expenses)
admin.site.register(ExpenseTypes)
admin.site.register(Keeper)