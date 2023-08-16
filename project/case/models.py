from django.db import models


class Case(models.Model):
    name = models.CharField(verbose_name="Название оружия", max_length=200)
    price = models.IntegerField()
    img = models.ImageField(upload_to='img/case/%Y-%m-%d/')
    weapons = models.JSONField()

    def get_absolute_url(self):
        return f"/personal-admin/case/{self.id}"

class Categories(models.Model):
    name = models.CharField(verbose_name="Название категории", max_length=200)
    position = models.IntegerField()
    cases_arr = models.JSONField()

    def get_absolute_url(self):
        return f"/personal-admin/categories/{self.id}"
