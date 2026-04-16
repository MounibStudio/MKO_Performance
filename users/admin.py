from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ('Extra Info', {'fields': ('telephone', 'adresse')}),
    )

    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Extra Info', {'fields': ('telephone', 'adresse')}),
    )

    list_display = ('id', 'username', 'email', 'telephone', 'is_staff', 'is_active')
    search_fields = ('username', 'email', 'telephone')
    list_filter = ('is_staff', 'is_active')