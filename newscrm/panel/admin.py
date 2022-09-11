from django.contrib import admin
from django.db import models
from django.forms import CheckboxSelectMultiple
from .models import User, Tema


@admin.register(User)
class GroupAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.ManyToManyField: {'widget': CheckboxSelectMultiple}
    }
    search_fields = ("name", "city", "subs", "kids", "animals", "tematika")
    ordering = ("name",)
    list_display = ['name', 'city', 'subs', 'link']


admin.site.register(Tema)
