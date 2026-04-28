from django.contrib import admin
from .models import Commande, ArticleCommande


class ArticleCommandeInline(admin.TabularInline):
    model = ArticleCommande
    extra = 0


@admin.register(Commande)
class CommandeAdmin(admin.ModelAdmin):
    list_display = ('id', 'utilisateur', 'total', 'statut', 'cree_le')
    list_filter = ('statut', 'cree_le')
    search_fields = ('id', 'utilisateur__nom_utilisateur')
    inlines = [ArticleCommandeInline]


@admin.register(ArticleCommande)
class ArticleCommandeAdmin(admin.ModelAdmin):
    list_display = ('id', 'commande', 'voiture', 'quantite', 'prix' ,'date_debut','date_fin')
    list_filter = ('commande',)