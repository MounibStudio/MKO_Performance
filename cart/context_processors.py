from cart.models import Panier, ArticlePanier

def panier_processor(request):
    nombre_items = 0
    total = 0
    
    if request.user.is_authenticated:
        try:
            panier = Panier.objects.get(utilisateur=request.user)
            articles = panier.articles.all()
            nombre_items = sum(a.quantite for a in articles)
            total = sum(a.voiture.prix * a.quantite for a in articles)
        except Panier.DoesNotExist:
            pass
    
    return {
        'nombre_items': nombre_items,
        'panier_total': total,
    }