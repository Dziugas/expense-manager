from django.contrib import admin
from .models import Expenses, ExpenseTypes

admin.site.register(Expenses)
admin.site.register(ExpenseTypes)