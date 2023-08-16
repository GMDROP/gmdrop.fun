from django.db import models


class UsersTelegram(models.Model):
    tg_id = models.IntegerField()
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255, blank=True)
    username = models.CharField(max_length=255)
    photo_url = models.CharField(max_length=255)


class SaleWeapons(models.Model):
    user_id = models.IntegerField()
    weapon_id = models.IntegerField()
    sale = models.BooleanField(default=False, verbose_name="Продано")


