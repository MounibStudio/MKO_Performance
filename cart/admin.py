from django.contrib import admin
from .models import Panier, ArticlePanier


class ArticlePanierInline(admin.TabularInline):
    model = ArticlePanier
    extra = 0


@admin.register(Panier)
class PanierAdmin(admin.ModelAdmin):
    list_display = ('id', 'utilisateur', 'cree_le')
    list_filter = ('cree_le',)
    inlines = [ArticlePanierInline]


@admin.register(ArticlePanier)
class ArticlePanierAdmin(admin.ModelAdmin):
    list_display = ('id', 'panier', 'voiture', 'quantite')
    list_filter = ('panier',)