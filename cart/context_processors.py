from cart.models import Panier, ArticlePanier
from orders.models import Commande

def panier_processor(request):
    nombre_items = 0
    total = 0
    mes_reservations = []
    
    if request.user.is_authenticated:
        try:
            panier = Panier.objects.get(utilisateur=request.user)
            articles = panier.articles.all()
            nombre_items = sum(a.quantite for a in articles)
            total = sum(a.voiture.prix * a.quantite for a in articles)
        except Panier.DoesNotExist:
            pass
        
        # Get user's reservations
        mes_reservations = Commande.objects.filter(
            utilisateur=request.user
        ).order_by('-cree_le')[:5]
    
    return {
        'nombre_items': nombre_items,
        'panier_total': total,
        'mes_reservations': mes_reservations,
    }