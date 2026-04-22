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
    image = models.ImageField(upload_to='voitures/')

    Category = models.ForeignKey(
        'products.Category',
        on_delete=models.CASCADE,
        related_name="voitures"
    )

    def __str__(self):
        return self.nom