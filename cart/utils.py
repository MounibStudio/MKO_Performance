from django.db import models
from datetime import date, timedelta

from products.models import Voiture
from orders.models import ArticleCommande


def dates_conflict(d1_start, d1_end, d2_start, d2_end):
    """Vérifie si deux intervalles de dates se chevauchent"""
    if d1_start is None or d1_end is None or d2_start is None or d2_end is None:
        return False
    return d1_start <= d2_end and d1_end >= d2_start


def est_voiture_disponible(voiture, date_debut, date_fin):
    """
    Vérifie si une voiture est disponible pour les dates données.
    Returns: (True, None) si disponible, (False, 'message_erreur') si non disponible
    """
    if date_debut is None or date_fin is None:
        return True, None
    
    if date_debut > date_fin:
        return False, "La date de fin doit être après la date de début."
    
    if date_debut < date.today():
        return False, "La date de début ne peut pas être dans le passé."
    
    reservations = ArticleCommande.objects.filter(
        voiture=voiture,
        date_fin__gte=date_debut,
        date_debut__lte=date_fin,
        commande__statut__in=['confirmee', 'en_attente']
    )
    
    total_reserve = sum(r.quantite for r in reservations)
    
    if total_reserve >= voiture.stock:
        return False, f"Cette voiture n'est pas disponible pour ces dates. Elle est déjà reservée."
    
    return True, None


def get_voitures_disponibles(date_debut, date_fin):
    """Retourne la liste des voitures disponibles pour les dates données"""
    if date_debut is None or date_fin is None:
        return Voiture.objects.all()
    
    unavailable_ids = []
    reservations = ArticleCommande.objects.filter(
        date_fin__gte=date_debut,
        date_debut__lte=date_fin,
        commande__statut__in=['confirmee', 'en_attente']
    )
    
    reserved_counts = {}
    for res in reservations:
        vid = res.voiture_id
        reserved_counts[vid] = reserved_counts.get(vid, 0) + res.quantite
    
    for voiture in Voiture.objects.all():
        reserve = reserved_counts.get(voiture.id, 0)
        if reserve < voiture.stock:
            unavailable_ids.append(voiture.id)
    
    return Voiture.objects.filter(id__in=unavailable_ids)


def get_dates_bloquees(voiture):
    """Retourne les dates déjà réservées pour une voiture"""
    reservations = ArticleCommande.objects.filter(
        voiture=voiture,
        commande__statut__in=['confirmee', 'en_attente']
    ).values_list('date_debut', 'date_fin')
    
    dates_bloquees = []
    for debut, fin in reservations:
        if debut and fin:
            current = debut
            while current <= fin:
                dates_bloquees.append(current)
                current += timedelta(days=1)
    
    return sorted(set(dates_bloquees))