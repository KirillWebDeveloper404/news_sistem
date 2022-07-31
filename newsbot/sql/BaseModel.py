from peewee import Model, SqliteDatabase


db = SqliteDatabase('../bot.db')

class BaseModel(Model):

    class Meta:
        database = db