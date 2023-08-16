from django.contrib import admin
from .models import *

class WeaponsAdmin(admin.ModelAdmin):
    list_display = ("name", "model_w", 'price', 'leg', 'stattrak')

admin.site.register(Weapons, WeaponsAdmin)
