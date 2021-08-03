from django import forms
from store.models import Recharge, Contacto

class RechargeForm(forms.ModelForm):
    
    class Meta:
        model = Recharge
        fields = "__all__"

class ContactoForm(forms.ModelForm):

    class Meta:
        model = Contacto
        fields= "__all__"