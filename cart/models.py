from django.db import models

class Panier(models.Model):
    utilisateur = models.ForeignKey(
        'users.User',
        on_delete=models.CASCADE,
        related_name="paniers"
    )
    cree_le = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Panier {self.id}"


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

    def __str__(self):
        return f"{self.voiture.nom} x {self.quantite}"