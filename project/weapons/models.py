from django.db import models

class Weapons(models.Model):
    LEG = (
        ('R', 'Rare'),
        ('E', 'Epic'),
        ('L', 'Legendary'),
        ('A', 'Arcane')
    )

    name = models.CharField(verbose_name="Название оружия", max_length=200)
    model_w = models.CharField(verbose_name="Модель оружия", max_length=200)
    price = models.IntegerField()
    img = models.ImageField(upload_to='img/weapons/%Y-%m-%d/')
    leg = models.CharField(max_length=1, choices=LEG, verbose_name="Редкость оружия")
    stattrak = models.BooleanField(default=False, verbose_name="StatTrak")

    def get_absolute_url(self):
        return f"/personal-admin/weapons/{self.id}"