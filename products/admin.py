from django.contrib import admin
from .models import Category, Voiture


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'nom', 'slug')
    search_fields = ('nom',)
    prepopulated_fields = {'slug': ('nom',)}


@admin.register(Voiture)
class VoitureAdmin(admin.ModelAdmin):
    list_display = ('id', 'nom', 'marque', 'modele', 'prix', 'stock', 'category')
    search_fields = ('nom', 'marque')
    list_filter = ('category',)