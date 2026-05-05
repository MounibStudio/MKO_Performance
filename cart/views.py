from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.conf import settings
from django.utils import timezone
from django.db import connection
from django.urls import reverse
from datetime import date

from .models import Panier, ArticlePanier
from orders.models import Commande, ArticleCommande
from products.models import Voiture
from .stripe_service import creer_session_paiement, creer_intent_paiement


def get_or_create_panier(user):
    panier, created = Panier.objects.get_or_create(utilisateur=user)
    return panier


@login_required
def panier_detail(request):
    panier = get_or_create_panier(request.user)
    articles = panier.articles.select_related('voiture')
    
    total = 0
    nombre_items = 0
    total_jours = 0
    
    for article in articles:
        jours = article.jours if article.date_debut and article.date_fin else 1
        total += article.voiture.prix * article.quantite * jours
        nombre_items += article.quantite
        total_jours = max(total_jours, jours)
    
    from datetime import date as date_module
    context = {
        'panier': panier,
        'articles': articles,
        'total': total,
        'nombre_items': nombre_items,
        'total_jours': total_jours,
        'today': date_module.today().isoformat(),
    }
    return render(request, 'cart/panier.html', context)


@require_POST
@login_required
def ajouter_au_panier(request, voiture_id):
    voiture = get_object_or_404(Voiture, id=voiture_id)
    
    date_debut_str = request.POST.get('date_debut')
    date_fin_str = request.POST.get('date_fin')
    
    if not date_debut_str or not date_fin_str:
        messages.error(request, "Veuillez choisir les dates de location.")
        return redirect('voiture_detail', pk=voiture_id)
    
    try:
        date_debut = date.fromisoformat(date_debut_str)
        date_fin = date.fromisoformat(date_fin_str)
    except ValueError:
        messages.error(request, "Dates invalides.")
        return redirect('voiture_detail', pk=voiture_id)
    
    panier = get_or_create_panier(request.user)
    
    article_existant = ArticlePanier.objects.filter(
        panier=panier, 
        voiture=voiture
    ).first()
    
    if article_existant:
        messages.warning(request, f"{voiture.nom} est déjà dans votre panier.")
        return redirect('cart:panier_detail')
    
    article, created = ArticlePanier.objects.get_or_create(
        panier=panier,
        voiture=voiture,
        defaults={
            'quantite': 1,
            'date_debut': date_debut,
            'date_fin': date_fin
        }
    )
    
    if not created:
        article.quantite += 1
        article.date_debut = date_debut
        article.date_fin = date_fin
        article.save()
        messages.success(request, f"🛒 {voiture.nom} ajouté au panier.")
    else:
        messages.success(request, f"🛒 {voiture.nom} ajouté au panier ({date_debut} au {date_fin}).")
    
    return redirect('cart:panier_detail')


@require_POST
@login_required
def modifier_dates(request):
    date_debut_str = request.POST.get('date_debut')
    date_fin_str = request.POST.get('date_fin')
    
    if not date_debut_str or not date_fin_str:
        messages.error(request, "Veuillez choisir les dates de location.")
        return redirect('cart:panier_detail')
    
    try:
        date_debut = date.fromisoformat(date_debut_str)
        date_fin = date.fromisoformat(date_fin_str)
    except ValueError:
        messages.error(request, "Dates invalides.")
        return redirect('cart:panier_detail')
    
    if date_debut > date_fin:
        messages.error(request, "La date de fin doit être après la date de début.")
        return redirect('cart:panier_detail')
    
    if date_debut < date.today():
        messages.error(request, "La date de début ne peut pas être dans le passé.")
        return redirect('cart:panier_detail')
    
    panier = get_or_create_panier(request.user)
    panier.date_debut = date_debut
    panier.date_fin = date_fin
    panier.save()
    
    messages.success(request, f"Dates mises à jour: {date_debut} au {date_fin}")
    return redirect('cart:panier_detail')


@require_POST
@login_required
def modifier_quantite(request, article_id):
    article = get_object_or_404(ArticlePanier, id=article_id, panier__utilisateur=request.user)
    nouvelle_quantite = int(request.POST.get('quantite', 1))
    
    if nouvelle_quantite < 1:
        article.delete()
        messages.success(request, f"✕ {article.voiture.nom} retiré du panier.")
    else:
        article.quantite = nouvelle_quantite
        article.save()
        messages.success(request, f"Quantité de {article.voiture.nom} mise à jour.")
    
    return redirect('cart:panier_detail')


@require_POST
@login_required
def supprimer_article(request, article_id):
    article = get_object_or_404(ArticlePanier, id=article_id, panier__utilisateur=request.user)
    nom_voiture = article.voiture.nom
    article.delete()
    
    panier = Panier.objects.filter(utilisateur=request.user).first()
    if panier and not panier.articles.exists():
        panier.date_debut = None
        panier.date_fin = None
        panier.save()
    
    messages.success(request, f"✕ {nom_voiture} retiré du panier.")
    return redirect('cart:panier_detail')


@require_POST
@login_required
def vider_panier(request):
    panier = get_or_create_panier(request.user)
    panier.articles.all().delete()
    panier.date_debut = None
    panier.date_fin = None
    panier.save()
    messages.success(request, "Panier vidé.")
    return redirect('cart:panier_detail')


@login_required
def get_panier_count(request):
    if not request.user.is_authenticated:
        return JsonResponse({'count': 0, 'total': 0})
    
    try:
        panier = Panier.objects.get(utilisateur=request.user)
        articles = panier.articles.all()
        count = sum(a.quantite for a in articles)
        
        total = sum(a.voiture.prix * a.quantite for a in articles)
        if panier.date_debut and panier.date_fin:
            jours = (panier.date_fin - panier.date_debut).days + 1
            total = total * jours
        
        return JsonResponse({'count': count, 'total': float(total)})
    except Panier.DoesNotExist:
        return JsonResponse({'count': 0, 'total': 0})


# ========== CHECKOUT ==========

@login_required
def checkout(request):
    """Page de réservation"""
    panier = Panier.objects.filter(utilisateur=request.user).first()
    
    if not panier or not panier.articles.exists():
        messages.error(request, "Votre panier est vide.")
        return redirect('cart:panier_detail')
    
    articles = panier.articles.select_related('voiture')
    
    total = 0
    for article in articles:
        jours = article.jours if article.date_debut and article.date_fin else 1
        total += article.voiture.prix * article.quantite * jours
    
    stripe_key = getattr(settings, 'STRIPE_SECRET_KEY', '')
    stripe_config = stripe_key and len(stripe_key) > 20
    
    context = {
        'panier': panier,
        'articles': articles,
        'total': total,
        'user': request.user,
        'stripe_configure': stripe_config,
        'stripe_publishable_key': getattr(settings, 'STRIPE_PUBLISHABLE_KEY', ''),
    }
    return render(request, 'cart/checkout.html', context)


@require_POST
@login_required
def passer_commande(request):
    """Valider la réservation"""
    paiement = request.POST.get('paiement')
    remarque = request.POST.get('remarque', '')
    
    if paiement not in ['cash', 'carte']:
        messages.error(request, "Veuillez choisir un mode de paiement.")
        return redirect('cart:checkout')
    
    panier = Panier.objects.filter(utilisateur=request.user).first()
    
    if not panier or not panier.articles.exists():
        messages.error(request, "Votre panier est vide.")
        return redirect('cart:panier_detail')
    
    articles = panier.articles.select_related('voiture')
    
    total = 0
    for article in articles:
        jours = article.jours if article.date_debut and article.date_fin else 1
        total += article.voiture.prix * article.quantite * jours
    
    stripe_configured = bool(settings.STRIPE_SECRET_KEY and len(settings.STRIPE_SECRET_KEY) > 20)
    
    if paiement == 'carte' and stripe_configured:
        try:
            commande = Commande.objects.create(
                utilisateur=request.user,
                total=total,
                statut='en_attente',
                remarque=remarque,
                paiement='carte'
            )
            
            for article in articles:
                jours = article.jours if article.date_debut and article.date_fin else 1
                cursor = connection.cursor()
                cursor.execute("SET SESSION sql_mode = ''")
                cursor.execute(
                    "INSERT INTO orders_articlecommande (commande_id, voiture_id, quantite, prix, date_debut, date_fin) VALUES (%s, %s, %s, %s, %s, %s)",
                    [commande.id, article.voiture.id, article.quantite, float(article.voiture.prix * jours), article.date_debut, article.date_fin]
                )
            
            result = creer_intent_paiement(total, commande.id)
            
            if 'error' in result:
                commande.statut = 'annulee'
                commande.save()
                return JsonResponse({'error': result['error']})
            
            commande.transaction_id = result['id']
            commande.save()
            
            return JsonResponse({
                'success': True,
                'client_secret': result['client_secret'],
                'commande_id': commande.id,
            })
        except Exception as e:
            return JsonResponse({'error': str(e)})
    
    else:
        # Paiement cash ou Stripe non configuré
        try:
            statut = 'en_attente' if paiement == 'cash' else 'confirmee'
            
            commande = Commande.objects.create(
                utilisateur=request.user,
                total=total,
                statut=statut,
                remarque=remarque,
                paiement=paiement
            )
            
            for article in articles:
                jours = article.jours if article.date_debut and article.date_fin else 1
                cursor = connection.cursor()
                cursor.execute("SET SESSION sql_mode = ''")
                cursor.execute(
                    "INSERT INTO orders_articlecommande (commande_id, voiture_id, quantite, prix, date_debut, date_fin) VALUES (%s, %s, %s, %s, %s, %s)",
                    [commande.id, article.voiture.id, article.quantite, float(article.voiture.prix * jours), article.date_debut, article.date_fin]
                )
            
            panier.articles.all().delete()
            panier.save()
            
            # Envoyer email de confirmation
            email_result = send_confirmation_email(commande, request.user)
            request.session['email_result'] = email_result
            
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': True,
                    'commande_id': commande.id,
                    'redirect': reverse('cart:confirmation', args=[commande.id])
                })
            
            messages.success(request, f"✅ Réservation #{commande.id} confirmée!")
            
            return redirect('cart:confirmation', commande_id=commande.id)
        except Exception as e:
            return JsonResponse({'error': str(e)})


# @require_POST - Removed for API compatibility
@csrf_exempt
def initialiser_paiement_stripe(request):
    """API pour initialiser le paiement Stripe"""
    import stripe
    from django.conf import settings
    
    stripe.api_key = settings.STRIPE_SECRET_KEY
    
    montant = request.POST.get('montant')
    commande_id = request.POST.get('commande_id', '0')
    
    if not montant:
        return JsonResponse({'success': False, 'message': 'Montant manquant'})
    
    try:
        montant = float(montant)
    except ValueError:
        return JsonResponse({'success': False, 'message': 'Montant invalide'})
    
    try:
        intent = stripe.PaymentIntent.create(
            amount=int(montant * 100),
            currency='mad',
            metadata={'commande_id': str(commande_id)},
            automatic_payment_methods={'enabled': True}
        )
        return JsonResponse({
            'success': True,
            'client_secret': intent.client_secret,
            'id': intent.id,
        })
    except stripe.error.StripeError as e:
        return JsonResponse({'success': False, 'message': str(e)})





@login_required
def confirmation(request, commande_id):
    """Page de confirmation"""
    from django.conf import settings
    import stripe
    
    commande = get_object_or_404(Commande, id=commande_id, utilisateur=request.user)
    
    if request.GET.get('success') == 'true' and commande.paiement == 'carte' and settings.STRIPE_SECRET_KEY:
        stripe.api_key = settings.STRIPE_SECRET_KEY
        
        if commande.transaction_id:
            try:
                intent = stripe.PaymentIntent.retrieve(commande.transaction_id)
                if intent.status == 'succeeded':
                    commande.statut = 'confirmee'
                    commande.save()
                    send_confirmation_email(commande, request.user)
            except stripe.error.StripeError:
                pass
    
    articles = commande.articles.select_related('voiture')
    
    email_result = request.session.pop('email_result', None)
    
    context = {
        'commande': commande,
        'articles': articles,
        'email_result': email_result,
    }
    return render(request, 'cart/confirmation.html', context)


@login_required
def mes_reservations(request):
    """Page listant toutes les réservations de l'utilisateur"""
    reservations = Commande.objects.filter(
        utilisateur=request.user
    ).order_by('-cree_le').prefetch_related('articles__voiture')
    
    context = {
        'reservations': reservations,
    }
    return render(request, 'cart/mes_reservations.html', context)


def send_confirmation_email(commande, user):
    """Envoyer email de confirmation de réservation"""
    import logging
    from django.core.mail import send_mail
    from django.conf import settings
    
    logger = logging.getLogger(__name__)
    
    if not user.email:
        logger.warning(f"Pas d'email pour l'utilisateur {user.id}")
        return "Pas d'email"
    
    try:
        vehicles = [a.voiture.nom for a in commande.articles.all()]
        vehicles_text = ", ".join(vehicles)
        
        sujet = f"Réservation #{commande.id} confirmée - MKO Performance"
        
        paiement_text = "Cash" if commande.paiement == 'cash' else "Carte" if commande.paiement == 'carte' else commande.paiement
        
        message = f"""Bonjour {user.first_name or user.username},

Votre réservation #{commande.id} a été confirmée.

Détails:
- Véhicule(s): {vehicles_text}
- Total: {commande.total} MAD
- Mode de paiement: {paiement_text}
- Date: {commande.cree_le.strftime('%d/%m/%Y à %H:%M')}

Merci de votre confiance!

L'équipe MKO Performance"""

        send_mail(
            sujet,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [user.email],
            fail_silently=False,
        )
        logger.info(f"Email de confirmation envoyé à {user.email}")
        return "Envoyé"
    except Exception as e:
        logger.error(f"Erreur envoi email: {e}")
        return f"Erreur: {e}"