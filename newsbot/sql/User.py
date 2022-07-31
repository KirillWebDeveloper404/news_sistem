from .BaseModel import BaseModel
from peewee import *


class User(BaseModel):
    # Анкета из тг
    name = CharField(max_length=100, unique=False)
    link = TextField(null=True, unique=False)
    city = CharField(max_length=50, null=True, unique=False)
    subs = IntegerField(null=True)

    # Данные из админки
    kids = TextField(null=True, unique=False)
    animals = TextField(null=True, unique=False)
    tematika = TextField(null=True, unique=False)

    # Системные переменные
    tg_id = CharField(max_length=50)
    apruve = BooleanField(null=True)

    class Meta:
        table_name = 'panel_user'
