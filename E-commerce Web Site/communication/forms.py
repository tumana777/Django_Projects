from django import forms
from .models import Smartphone

class SmartphoneForm(forms.ModelForm):
    class Meta:
        model = Smartphone
        exclude = ["category"]