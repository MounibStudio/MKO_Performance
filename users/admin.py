from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    # Formulaire d'édition
    fieldsets = UserAdmin.fieldsets + (
        ('Informations supplémentaires', {'fields': ('phone', 'address')}),
    )
    # Formulaire d'ajout
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Informations supplémentaires', {'fields': ('email', 'phone', 'address')}),
    )