from django.urls import path
from . import views

app_name = 'cart'

urlpatterns = [
    path('', views.panier_detail, name='panier_detail'),
    path('ajouter/<int:voiture_id>/', views.ajouter_au_panier, name='ajouter_au_panier'),
    path('modifier-dates/', views.modifier_dates, name='modifier_dates'),
    path('modifier/<int:article_id>/', views.modifier_quantite, name='modifier_quantite'),
    path('supprimer/<int:article_id>/', views.supprimer_article, name='supprimer_article'),
    path('vider/', views.vider_panier, name='vider_panier'),
    path('count/', views.get_panier_count, name='get_panier_count'),
    path('checkout/', views.checkout, name='checkout'),
    path('passer-commande/', views.passer_commande, name='passer_commande'),
    path('initialiser-paiement/', views.initialiser_paiement_stripe, name='initialiser_paiement'),
    path('confirmation/<int:commande_id>/', views.confirmation, name='confirmation'),
    path('mes-reservations/', views.mes_reservations, name='mes_reservations'),
]