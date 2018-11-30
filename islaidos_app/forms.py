from django import forms
from .models import Islaidos

class IslaidosForm(forms.ModelForm):
    class Meta:
        model = Islaidos
        fields = ['data', 'tipas', 'tiekejas', 'dok_nr', 'suma']