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