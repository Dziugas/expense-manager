from django import forms
from django.forms import DateInput
from .models import Expenses, ExpenseTypes, Keeper

class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expenses
        fields = ['data', 'tipas', 'description', 'tiekejas', 'dok_nr', 'suma', 'keeper']
        widgets = {
            'data': DateInput(attrs={'type': 'date'}),
        }

class ExpenseTypeForm(forms.ModelForm):

    class Meta:
        model = ExpenseTypes
        fields = ['tipas', 'keeper']

class KeeperForm(forms.ModelForm):
    class Meta:
        model = Keeper
        fields = ['keeper_name', 'user_name']
