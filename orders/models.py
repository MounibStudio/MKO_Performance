from django.db import models
from django.core.exceptions import ValidationError

class Commande(models.Model):
    utilisateur = models.ForeignKey(
        'users.User',
        on_delete=models.CASCADE,
        related_name="commandes"
    )

    total = models.DecimalField(max_digits=10, decimal_places=2)
    statut = models.CharField(max_length=50)
    cree_le = models.DateTimeField(auto_now_add=True)
    remarque = models.TextField(blank=True, default='')
    paiement = models.CharField(max_length=20, blank=True, default='')
    transaction_id = models.CharField(max_length=50, blank=True, default='')

    def __str__(self):
        return f"Commande {self.id}"

   


class ArticleCommande(models.Model):
    date_debut = models.DateTimeField(null=True, blank=True)
    date_fin   =  models.DateTimeField(null=True, blank=True)

    commande = models.ForeignKey(
        'orders.Commande',
        on_delete=models.CASCADE,
        related_name="articles"
    )

    voiture = models.ForeignKey(
        'products.Voiture',
        on_delete=models.CASCADE
    )

    quantite = models.PositiveIntegerField()
    prix = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.voiture.nom} x {self.quantite}"  
    
    
    
    def clean(self):
        if self.date_debut and self.date_fin:
            if self.date_fin < self.date_debut:
                raise ValidationError(
                    "La date de fin doit être après la date de début."
                ) 