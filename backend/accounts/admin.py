from django.contrib import admin
from .models import AdminUser, NormalUser
from typing import *

# Register your models here.


@admin.register(AdminUser)
class UserAdmin(admin.ModelAdmin):
    search_fields = ["name"]
    list_display = ["name", "email", "last_login", "created_at", "updated_at"]
    list_display_links = ["name"]    


@admin.register(NormalUser)
class NormalAdmin(admin.ModelAdmin):
    search_fields = ["username"]
    list_display = ["username", "email", "created_at", "updated_at"]
    list_display_links = ["username"]    