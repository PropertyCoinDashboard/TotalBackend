from django.contrib import admin
from .models import AdminUser, NormalUser

# Register your models here.


@admin.register(AdminUser)
class UserAdmin(admin.ModelAdmin):
    search_fields = ["name"]
    list_display = ["name", "email", "last_login", "created_at", "updated_at"]
    list_display_links = ["name"]
