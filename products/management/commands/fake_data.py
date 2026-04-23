from django.core.management.base import BaseCommand
from faker import Faker
from products.models import Category, Voiture
import random

class Command(BaseCommand):
    help = 'Génère les données fictives pour les voitures'

    def handle(self, *args, **options):
        faker = Faker('fr_FR')

        categories = ['Berline', 'SUV', 'Compacte', 'Luxe', 'Familiale']
        for nom in categories:
            Category.objects.get_or_create(
                nom=nom,
                defaults={'slug': faker.slug()}
            )
            self.stdout.write(f'Catégorie créée: {nom}')

        cat_list = list(Category.objects.all())
        for i in range(8):
            marque = random.choice(['Renault', 'Peugeot', 'BMW', 'Mercedes', 'Audi'])
            voiture = Voiture.objects.create(
                nom=f'{marque} {faker.word().capitalize()}',
                marque=marque,
                modele=random.randint(2018, 2025),
                transmission=random.choice(['Manuelle', 'Automatique']),
                description=faker.text(max_nb_chars=450),
                prix=faker.random_number(digits=4) + 50,
                stock=faker.random_int(min=0, max=20),
                image_exterieur='voitures/exterieur/default.jpg',
                image_interieur='voitures/interieur/default.jpg',
                Category=random.choice(cat_list)
            )
            self.stdout.write(f'Voiture {i+1} créée: {voiture.nom}')