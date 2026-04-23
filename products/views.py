from django.shortcuts import render
from django.views import View
from .models import Voiture, Category

class ProductListView(View):
    def get(self, request):
        voitures = Voiture.objects.all().select_related('Category')
        categories = Category.objects.all()
        return render(request, 'products/product_list.html', {
            'voitures': voitures,
            'categories': categories
        })