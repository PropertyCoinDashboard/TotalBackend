from django.contrib import admin
from .models import User
from typing import *

# Register your models here.


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    search_fields: Sequence[str] = ["name"]
    list_display = ["name", "email", "last_login", "created_at", "updated_at"]
    list_display_links = ["name"]    
