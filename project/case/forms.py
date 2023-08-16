from django import forms
from .models import *


class CaseForm(forms.ModelForm):
    name = forms.CharField()
    price = forms.IntegerField()
    img = forms.ImageField()
    weapons = forms.JSONField()

    class Meta:
        model = Case
        fields = '__all__'

class CategoriesForm(forms.ModelForm):
    name = forms.CharField()
    position = models.IntegerField()
    cases_arr = models.JSONField()

    class Meta:
        model = Categories
        fields = '__all__'