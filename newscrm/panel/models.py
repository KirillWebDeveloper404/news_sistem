from django.db import models


class Stat(models.Model):
    date = models.CharField(max_length=20)
    count = models.CharField(max_length=10)

    class Meta:
        verbose_name = 'Статистика'

class Tema(models.Model):
    name = models.CharField(max_length=150)

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = 'Тематика'
        verbose_name_plural = 'Тематика'

class User(models.Model):
    # Анкета из тг
    name = models.CharField(max_length=100, unique=False)
    link = models.TextField(null=True, unique=False)
    city = models.CharField(max_length=50, null=True, unique=False)
    subs = models.IntegerField(null=True)

    # Данные из админки
    kids = models.BooleanField(null=True)
    animals = models.BooleanField(null=True)
#    tematika = models.TextField(null=True, unique=False)
    # tema = models.ForeignKey(to=Tema, on_delete=models.SET_NULL, null=True, verbose_name='Тематика(выбор)')
    tema = models.ManyToManyField(to=Tema, verbose_name='Тематика(выбор)', db_table='panel_user_panel_tema_through')
    sex = models.CharField(max_length=10,
        choices=(
        ('m', 'Муж'),
        ('w', 'Жен')
    ), 
    null=True, blank=True, 
    verbose_name='Пол')
    phone = models.TextField(null=True, blank=True)

    # Системные переменные
    tg_id = models.CharField(max_length=50)
    apruve = models.BooleanField(null=True)

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
