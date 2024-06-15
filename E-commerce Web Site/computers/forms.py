from django import forms
from .models import Laptop, PC, Tablet, PartsOrAccessories

class PCForm(forms.ModelForm):
    class Meta:
        model = PC
        exclude = ["category", "owner"]
        
class LaptopForm(forms.ModelForm):
    class Meta:
        model = Laptop
        exclude = ["category", "owner"]
        
class TabletForm(forms.ModelForm):
    class Meta:
        model = Tablet
        exclude = ["category", "owner"]

class PartsOrAccessoriesForm(forms.ModelForm):
    class Meta:
        model = PartsOrAccessories
        exclude = ["subcategory", "owner"]