from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ('username', 'email', 'role', 'phone', 'shop_name', 'is_verified', 'is_staff', 'is_active')
    list_filter = ('role', 'is_verified', 'is_staff', 'is_active')
    search_fields = ("username", "email", "phone", "shop_name")
    ordering = ('username',)
    fieldsets = BaseUserAdmin.fieldsets + (
        ("Qo'shimcha malumotlar", {"fields": ("role", "phone", "address", "avatar", "shop_name", "is_verified")}),
    )
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        ("Qo'shimcha malumotlar", {"fields": ("role", "phone", "address", "avatar", "shop_name")}),
    )