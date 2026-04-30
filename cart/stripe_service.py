import os
import stripe
from django.conf import settings

# Configuration Stripe
STRIPE_SECRET_KEY = getattr(settings, 'STRIPE_SECRET_KEY', '')
STRIPE_PUBLISHABLE_KEY = getattr(settings, 'STRIPE_PUBLISHABLE_KEY', '')
STRIPE_WEBHOOK_SECRET = getattr(settings, 'STRIPE_WEBHOOK_SECRET', '')

stripe.api_key = STRIPE_SECRET_KEY


def creer_session_paiement(commande, articles, panier):
    """
    Crée une session de paiement Stripe pour une commande
    """
    liste_articles = []
    
    for article in articles:
        liste_articles.append({
            'price_data': {
                'currency': 'mad',
                'product_data': {
                    'name': article.voiture.nom,
                    'description': f"Location du {panier.date_debut} au {panier.date_fin}",
                },
                'unit_amount': int(article.voiture.prix * 100),  # En centimes
            },
            'quantity': article.quantite,
        })
    
    # Ajouter les jours de location
    jours = (panier.date_fin - panier.date_debut).days + 1
    if jours > 1:
        liste_articles.append({
            'price_data': {
                'currency': 'mad',
                'product_data': {
                    'name': f'Location ({jours} jours)',
                },
                'unit_amount': 0,  # Inclus dans le prix
            },
            'quantity': jours - 1,
        })
    
    try:
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=liste_articles,
            mode='payment',
            success_url=f'{settings.SITE_URL}/panier/confirmation/{commande.id}/?success=true',
            cancel_url=f'{settings.SITE_URL}/panier/checkout/?canceled=true',
            client_reference_id=str(commande.id),
            metadata={
                'commande_id': str(commande.id),
                'utilisateur_id': str(commande.utilisateur_id),
            },
        )
        return session
    except stripe.error.StripeError as e:
        return {'error': str(e)}


def verifier_paiement(session_id):
    """
    Vérifie le statut d'un paiement Stripe
    """
    try:
        session = stripe.checkout.Session.retrieve(session_id)
        return {
            'status': session.payment_status,
            'id': session.id,
        }
    except stripe.error.StripeError as e:
        return {'error': str(e)}


def creer_intent_paiement(montant, commande_id):
    """
    Crée un PaymentIntent pour paiement direct (plus flexible)
    """
    try:
        intent = stripe.PaymentIntent.create(
            amount=int(montant * 100),  # En centimes
            currency='mad',
            metadata={
                'commande_id': str(commande_id),
            },
        )
        return {
            'client_secret': intent.client_secret,
            'id': intent.id,
        }
    except stripe.error.StripeError as e:
        return {'error': str(e)}


def traiter_webhook(request):
    """
    Traite un webhook Stripe
    """
    payload = request.body
    sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')
    
    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, STRIPE_WEBHOOK_SECRET
        )
    except ValueError:
        return {'error': 'Invalid payload'}
    except stripe.error.SignatureVerificationError:
        return {'error': 'Invalid signature'}
    
    # Traiter les événements
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        commande_id = session.get('client_reference_id')
        # Mettre à jour le statut de la commande
        from orders.models import Commande
        try:
            commande = Commande.objects.get(id=commande_id)
            commande.statut = 'confirmee'
            commande.transaction_id = session.id
            commande.save()
        except Commande.DoesNotExist:
            pass
    
    elif event['type'] == 'payment_intent.succeeded':
        intent = event['data']['object']
        commande_id = intent.get('metadata', {}).get('commande_id')
        if commande_id:
            from orders.models import Commande
            try:
                commande = Commande.objects.get(id=commande_id)
                commande.statut = 'confirmee'
                commande.transaction_id = intent.id
                commande.save()
            except Commande.DoesNotExist:
                pass
    
    return {'status': 'success'}