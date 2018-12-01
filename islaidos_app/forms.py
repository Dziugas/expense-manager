from django import forms
from .models import Islaidos, Islaidu_tipai

class IslaidosForm(forms.ModelForm):
    class Meta:
        model = Islaidos
        fields = ['data', 'tipas', 'tiekejas', 'dok_nr', 'suma']

class TiekejaiForm(forms.ModelForm):
    class Meta:
        model = Islaidu_tipai
        fields = ['tipas', 'aktyvus']