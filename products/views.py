from django.shortcuts import render, get_object_or_404
from django.views import View
from .models import Voiture, Category
from orders.models import ArticleCommande


class ProductListView(View):
    def get(self, request):
        voitures = Voiture.objects.all().select_related('category')
        categories = Category.objects.all()

        voitures_reservees = set(
            ArticleCommande.objects.values_list('voiture_id', flat=True)
        )

        prix_list = voitures.values_list('prix', flat=True)
        max_price = int(max(prix_list)) if prix_list else 5000

        return render(request, 'products/product_list.html', {
            'voitures': voitures,
            'categories': categories,
            'max_price': max_price,
            'voitures_reservees': voitures_reservees,
        })


class VoitureDetailView(View):
    def get(self, request, pk):
        voiture = get_object_or_404(Voiture, pk=pk)

        similaires = Voiture.objects.filter(
            category=voiture.category
        ).exclude(pk=voiture.pk)[:3]

        est_reservee = ArticleCommande.objects.filter(voiture=voiture).exists()

        return render(request, 'products/voiture_detail.html', {
            'voiture': voiture,
            'similaires': similaires,
            'est_reservee': est_reservee,
        })