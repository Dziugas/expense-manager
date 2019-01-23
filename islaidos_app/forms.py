from django import forms
from django.forms import DateInput
from .models import Expenses, ExpenseTypes

class IslaidosForm(forms.ModelForm):
    class Meta:
        model = Expenses
        fields = ['data', 'tipas', 'tiekejas', 'dok_nr', 'suma']
        widgets = {
            'data': DateInput(attrs={'type': 'date'}),
        }

class TiekejaiForm(forms.ModelForm):
    class Meta:
        model = ExpenseTypes
        fields = ['tipas', 'aktyvus']