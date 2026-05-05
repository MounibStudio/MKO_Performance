from django.db import models


class Category(models.Model):
    nom = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.nom


class Voiture(models.Model):
    nom = models.CharField(max_length=100)
    marque = models.CharField(max_length=100)
    modele = models.PositiveIntegerField()
    transmission = models.CharField(max_length=50)
    description = models.TextField()
    prix = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField()
    image_exterieur = models.ImageField(upload_to='voitures/exterieur/', max_length=500)
    image_interieur = models.ImageField(upload_to='voitures/interieur/', max_length=500)

    category = models.ForeignKey(
        'products.Category',
        on_delete=models.CASCADE,
        related_name="voitures"
    )

    def __str__(self):
        return self.nom


class Review(models.Model):
    voiture = models.ForeignKey(
        'products.Voiture',
        on_delete=models.CASCADE,
        related_name="reviews"
    )
    utilisateur = models.ForeignKey(
        'users.User',
        on_delete=models.CASCADE,
        related_name="reviews"
    )
    note = models.PositiveIntegerField(choices=[(i, i) for i in range(1, 6)])
    commentaire = models.TextField()
    cree_le = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('voiture', 'utilisateur')
        ordering = ['-cree_le']

    def __str__(self):
        return f"{self.utilisateur.username} - {self.voiture.nom} - {self.note}⭐"


class Article(models.Model):
    titre = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    contenu = models.TextField()
    image = models.ImageField(upload_to='blog/', blank=True, null=True)
    statut = models.CharField(max_length=20, choices=[('publie', 'Publié'), ('brouillon', 'Brouillon')], default='publie')
    cree_le = models.DateTimeField(auto_now_add=True)
    modifie_le = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-cree_le']

    def __str__(self):
        return self.titre