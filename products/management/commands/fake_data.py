from django.core.management.base import BaseCommand
from products.models import Category, Voiture

class Command(BaseCommand):
    help = 'Génère les données fictives pour les voitures MKO Performance'

    def handle(self, *args, **options):
        categories_data = [
            {'nom': 'Berline', 'slug': 'berline'},
            {'nom': 'SUV', 'slug': 'suv'},
            {'nom': 'Compacte', 'slug': 'compacte'},
            {'nom': 'Luxe', 'slug': 'luxe'},
            {'nom': 'Familiale', 'slug': 'familiale'},
        ]

        for cat_data in categories_data:
            cat, created = Category.objects.get_or_create(
                slug=cat_data['slug'],
                defaults={'nom': cat_data['nom']}
            )
            status = 'créée' if created else 'existe déjà'
            self.stdout.write(f'Catégorie {cat.nom} {status}')

        voitures_data = [
            {
                'nom': 'BMW Série 3',
                'marque': 'BMW',
                'modele': 2024,
                'transmission': 'Automatique',
                'description': 'Berline élégante et sportive, parfaite pour les déplacements urbains et les longs voyages. Equipée du système iDrive et d\'aides à la conduite avancées.',
                'prix': 45000.00,
                'stock': 5,
                'image_exterieur': 'voitures/39638.jpg',
                'image_interieur': 'voitures/39638.jpg',
                'category_slug': 'luxe'
            },
            {
                'nom': 'Mercedes Classe A',
                'marque': 'Mercedes-Benz',
                'modele': 2023,
                'transmission': 'Automatique',
                'description': 'Compacte premium avec un intérieur raffiné et des technologies de pointe. Idéal pour les professionnels recherchant le confort.',
                'prix': 42000.00,
                'stock': 3,
                'image_exterieur': 'voitures/39638.jpg',
                'image_interieur': 'voitures/39638.jpg',
                'category_slug': 'compacte'
            },
            {
                'nom': 'Renault Clio',
                'marque': 'Renault',
                'modele': 2024,
                'transmission': 'Manuelle',
                'description': 'Citadine économique et agile, parfaite pour la ville. Faible consommation de carburant et facilités de stationnement.',
                'prix': 18000.00,
                'stock': 10,
                'image_exterieur': 'voitures/39638.jpg',
                'image_interieur': 'voitures/39638.jpg',
                'category_slug': 'compacte'
            },
            {
                'nom': 'Peugeot 3008',
                'marque': 'Peugeot',
                'modele': 2023,
                'transmission': 'Automatique',
                'description': 'SUV familial spacieux avec un design moderne et une habitabilitéExceptionnelle. Parfait pour les escapades en famille.',
                'prix': 35000.00,
                'stock': 6,
                'image_exterieur': 'voitures/39638.jpg',
                'image_interieur': 'voitures/39638.jpg',
                'category_slug': 'suv'
            },
            {
                'nom': 'Audi A4',
                'marque': 'Audi',
                'modele': 2024,
                'transmission': 'Automatique',
                'description': 'Berline sportive combines elegance et performance. Technologie de pointe avec un confort de conduite incomparable.',
                'prix': 52000.00,
                'stock': 4,
                'image_exterieur': 'voitures/39638.jpg',
                'image_interieur': 'voitures/39638.jpg',
                'category_slug': 'luxe'
            },
            {
                'nom': 'Volkswagen Tiguan',
                'marque': 'Volkswagen',
                'modele': 2023,
                'transmission': 'Automatique',
                'description': 'SUV polyvalent adapté à toutes les conditions. Grand coffre et habitacle confortable pour les longues distances.',
                'prix': 38000.00,
                'stock': 7,
                'image_exterieur': 'voitures/39638.jpg',
                'image_interieur': 'voitures/39638.jpg',
                'category_slug': 'suv'
            },
            {
                'nom': 'Toyota Corolla',
                'marque': 'Toyota',
                'modele': 2024,
                'transmission': 'Hybride',
                'description': 'Hybride fiable et économique. Reference en termes de consommation et de fiabilité automobile.',
                'prix': 28000.00,
                'stock': 12,
                'image_exterieur': 'voitures/39638.jpg',
                'image_interieur': 'voitures/39638.jpg',
                'category_slug': 'familiale'
            },
            {
                'nom': 'Skoda Octavia',
                'marque': 'Skoda',
                'modele': 2023,
                'transmission': 'Manuelle',
                'description': 'Familiale spacieuse avec un rapport qualité-prix excellent. Grand volume de chargement et confort de route.',
                'prix': 25000.00,
                'stock': 8,
                'image_exterieur': 'voitures/39638.jpg',
                'image_interieur': 'voitures/39638.jpg',
                'category_slug': 'familiale'
            },
        ]

        for v_data in voitures_data:
            category = Category.objects.get(slug=v_data['category_slug'])
            v_data.pop('category_slug')
            v_data['Category'] = category

            voiture, created = Voiture.objects.get_or_create(
                nom=v_data['nom'],
                defaults=v_data
            )
            status = 'créée' if created else 'existe déjà'
            self.stdout.write(f'Voiture {voiture.nom} {status}')

        self.stdout.write(self.style.SUCCESS('Données MKO Performance créées avec succès!'))