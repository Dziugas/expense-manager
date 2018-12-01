from django import forms
from django.forms import DateInput
from .models import Islaidos, Islaidu_tipai

class IslaidosForm(forms.ModelForm):
    class Meta:
        model = Islaidos
        fields = ['data', 'tipas', 'tiekejas', 'dok_nr', 'suma']
        widgets = {
            'data': DateInput(attrs={'type': 'date'}),
        }

class TiekejaiForm(forms.ModelForm):
    class Meta:
        model = Islaidu_tipai
        fields = ['tipas', 'aktyvus']