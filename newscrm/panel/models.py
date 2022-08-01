from django.db import models


class User(models.Model):
    # Анкета из тг
    name = models.CharField(max_length=100, unique=False)
    link = models.TextField(null=True, unique=False)
    city = models.CharField(max_length=50, null=True, unique=False)
    subs = models.IntegerField(null=True)

    # Данные из админки
    kids = models.BooleanField(null=True)
    animals = models.BooleanField(null=True)
    tematika = models.TextField(null=True, unique=False)

    # Системные переменные
    tg_id = models.CharField(max_length=50)
    apruve = models.BooleanField(null=True)

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
