from django.contrib import admin
from .models import Category,Product

# Register your models here.

@admin.register(Category)
class Category (admin.ModelAdmin):
    prepopulated_fields={'slug':('name',)}


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display=('name','category','price','stock')
    list_filter=('category',)
    search_fields=('name','description')

