from django.shortcuts import render
from django.views import View
from .data import products  # On importe la liste 'produits' du fichier envoyé par le prof

class ProductListView(View):
    def get(self, request):
        # On crée un dictionnaire 'context' pour passer les données au template
        return render(request, 'products/product_list.html', {'products': products})