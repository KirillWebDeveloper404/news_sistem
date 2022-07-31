from django.contrib import admin
from .models import User


@admin.register(User)
class GroupAdmin(admin.ModelAdmin):
    search_fields = ("name", "city", "subs", "kids", "animals", "tematika")
    ordering = ("name",)
    list_display = ['name', 'city', 'subs', 'link']