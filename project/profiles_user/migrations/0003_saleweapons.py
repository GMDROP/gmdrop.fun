# Generated by Django 4.2.3 on 2023-07-31 03:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles_user', '0002_alter_userstelegram_last_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='SaleWeapons',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.IntegerField()),
                ('weapon_id', models.IntegerField()),
                ('sale', models.BooleanField(default=False, verbose_name='Продано')),
            ],
        ),
    ]
