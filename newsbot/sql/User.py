from .BaseModel import BaseModel
from peewee import *


class Tema(BaseModel):
    name = CharField(max_length=150)

    class Meta:
        table_name = 'panel_tema'


class Stat(BaseModel):
    date = CharField(max_length=20)
    count = CharField(max_length=20)

    class Meta:
        table_name = 'panel_stat'


class User(BaseModel):
    # Анкета из тг
    name = CharField(max_length=100, unique=False)
    link = TextField(null=True, unique=False)
    city = CharField(max_length=50, null=True, unique=False)
    subs = IntegerField(null=True)

    # Данные из админки
    kids = BooleanField(null=True)
    animals = BooleanField(null=True)
#    tematika = TextField(null=True, unique=False)
    # tema = ForeignKey(to=Tema, on_delete=SET_NULL, null=True, verbose_name='Тематика(выбор)')
    tema = ManyToManyField(model=Tema)
    sex = CharField(max_length=10, null=True)
    phone = TextField(null=True)

    # Системные переменные
    tg_id = CharField(max_length=50)
    apruve = BooleanField(null=True)

    class Meta:
        table_name = 'panel_user'
