from django.shortcuts import render, get_object_or_404
from django.views import View
from datetime import date, timedelta
from .models import Voiture, Category
from orders.models import ArticleCommande


class ProductListView(View):
    def get(self, request):
        today = date.today().isoformat()
        
        voitures = Voiture.objects.all().select_related('category')
        categories = Category.objects.all()

        prix_list = voitures.values_list('prix', flat=True)
        max_price = int(max(prix_list)) if prix_list else 5000

        return render(request, 'products/product_list.html', {
            'voitures': voitures,
            'categories': categories,
            'max_price': max_price,
            'today': today,
        })


class VoitureDetailView(View):
    def get(self, request, pk):
        today = date.today().isoformat()
        voiture = get_object_or_404(Voiture, pk=pk)

        similaires = Voiture.objects.filter(
            category=voiture.category
        ).exclude(pk=voiture.pk)[:3]
        
        blocked_dates = []
        today_date = date.today()
        reservations = ArticleCommande.objects.filter(
            voiture=voiture,
            commande__statut__in=['confirmee', 'en_attente']
        )
        for res in reservations:
            if res.date_debut and res.date_fin:
                current = res.date_debut.date() if hasattr(res.date_debut, 'date') else res.date_debut
                end = res.date_fin.date() if hasattr(res.date_fin, 'date') else res.date_fin
                while current <= end:
                    if current >= today_date:
                        blocked_dates.append(current.isoformat())
                    current += timedelta(days=1)

        return render(request, 'products/voiture_detail.html', {
            'voiture': voiture,
            'similaires': similaires,
            'today': today,
            'blocked_dates': blocked_dates,
        })