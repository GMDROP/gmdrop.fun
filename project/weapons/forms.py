from django import forms
from .models import *


class WeaponsForm(forms.ModelForm):
    name = forms.CharField()
    model_w = forms.CharField()
    price = forms.IntegerField()
    img = forms.ImageField()
    leg = forms.CharField()
    stattrak = forms.BooleanField()

    class Meta:
        model = Weapons
        fields = '__all__'