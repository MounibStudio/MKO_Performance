from django.db import models
from datetime import date


class Panier(models.Model):
    utilisateur = models.ForeignKey(
        'users.User',
        on_delete=models.CASCADE,
        related_name="paniers"
    )
    cree_le = models.DateTimeField(auto_now_add=True)

    date_debut = models.DateField(null=True, blank=True)
    date_fin = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"Panier {self.id} - {self.utilisateur.username}"


def dates_conflict(d1_start, d1_end, d2_start, d2_end):
    if d1_start is None or d1_end is None or d2_start is None or d2_end is None:
        return False
    return d1_start <= d2_end and d1_end >= d2_start


class ArticlePanier(models.Model):
    panier = models.ForeignKey(
        'cart.Panier',
        on_delete=models.CASCADE,
        related_name="articles"
    )

    voiture = models.ForeignKey(
        'products.Voiture',
        on_delete=models.CASCADE
    )

    quantite = models.PositiveIntegerField()
    date_debut = models.DateField(null=True, blank=True)
    date_fin = models.DateField(null=True, blank=True)

    @property
    def jours(self):
        if self.date_debut and self.date_fin:
            return (self.date_fin - self.date_debut).days + 1
        return 1

    @property
    def total(self):
        return self.voiture.prix * self.quantite * self.jours

    def __str__(self):
        return f"{self.voiture.nom} x {self.quantite}"