from django.core.management.base import BaseCommand
from products.models import Category, Voiture

class Command(BaseCommand):
    help = 'Génère les données pour les voitures MKO Performance'

    def handle(self, *args, **options):
        categories_data = [
            {'nom': 'Berline', 'slug': 'berline'},
            {'nom': 'SUV', 'slug': 'suv'},
            {'nom': 'Coupé', 'slug': 'coupe'},
            {'nom': 'Sport', 'slug': 'sport'},
            {'nom': 'Luxe', 'slug': 'luxe'},
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
                'description': 'Berline élégante et sportive, parfaite pour les déplacements urbains et les longs voyages.',
                'prix': 45000.00,
                'stock': 5,
                'image_exterieur': 'products/Sedans/bmw/exterior.jpg',
                'image_interieur': 'products/Sedans/bmw/interior.jpg',
                'category_slug': 'berline'
            },
            {
                'nom': 'Mercedes-Benz Classe C',
                'marque': 'Mercedes-Benz',
                'modele': 2023,
                'transmission': 'Automatique',
                'description': 'Berline premium avec un intérieur raffiné et des technologies de pointe.',
                'prix': 48000.00,
                'stock': 4,
                'image_exterieur': 'products/Sedans/mercedes/exterior.jpg',
                'image_interieur': 'products/Sedans/mercedes/interior.jpg',
                'category_slug': 'luxe'
            },
            {
                'nom': 'Audi A4',
                'marque': 'Audi',
                'modele': 2024,
                'transmission': 'Automatique',
                'description': 'Berline sportive combines élégance et performance avec un confort incomparable.',
                'prix': 52000.00,
                'stock': 3,
                'image_exterieur': 'products/Sedans/audi/exterior.jpg',
                'image_interieur': 'products/Sedans/audi/interior.jpg',
                'category_slug': 'luxe'
            },
            {
                'nom': 'BMW X5',
                'marque': 'BMW',
                'modele': 2023,
                'transmission': 'Automatique',
                'description': 'SUV familial spacieux avec un design moderne et une habitabilité exceptionnelle.',
                'prix': 65000.00,
                'stock': 6,
                'image_exterieur': 'products/SUV/bmw/exteriror.webp',
                'image_interieur': 'products/SUV/bmw/interior.webp',
                'category_slug': 'suv'
            },
            {
                'nom': 'Mercedes GLE',
                'marque': 'Mercedes-Benz',
                'modele': 2024,
                'transmission': 'Automatique',
                'description': 'SUV luxueux combinant performance et confort pour les longues distances.',
                'prix': 72000.00,
                'stock': 4,
                'image_exterieur': 'products/SUV/mercedes/exteriro.webp',
                'image_interieur': 'products/SUV/mercedes/interiro.webp',
                'category_slug': 'suv'
            },
            {
                'nom': 'Audi Q7',
                'marque': 'Audi',
                'modele': 2023,
                'transmission': 'Automatique',
                'description': 'SUV spacieux et élégant, idéal pour les familles et les voyages.',
                'prix': 58000.00,
                'stock': 5,
                'image_exterieur': 'products/SUV/audi/exterior.jpg',
                'image_interieur': 'products/SUV/audi/interiro.jpg',
                'category_slug': 'suv'
            },
            {
                'nom': 'BMW Série 4 Coupé',
                'marque': 'BMW',
                'modele': 2024,
                'transmission': 'Automatique',
                'description': 'Coupé sportif avec un design dynamique et des performances impressionnantes.',
                'prix': 55000.00,
                'stock': 4,
                'image_exterieur': 'products/Coupe/bmw/exterior.jpg',
                'image_interieur': 'products/Coupe/bmw/interior.jpg',
                'category_slug': 'coupe'
            },
            {
                'nom': 'Mercedes CLE',
                'marque': 'Mercedes-Benz',
                'modele': 2024,
                'transmission': 'Automatique',
                'description': 'Coupé élégant alliant luxe et sportivité pour les amateurs de design.',
                'prix': 62000.00,
                'stock': 3,
                'image_exterieur': 'products/Coupe/mercedes/exterior.jpg',
                'image_interieur': 'products/Coupe/mercedes/interior.jpg',
                'category_slug': 'coupe'
            },
            {
                'nom': 'BMW M8',
                'marque': 'BMW',
                'modele': 2024,
                'transmission': 'Automatique',
                'description': 'Sportive d\'exception avec un moteur puissant et un luxe incomparable.',
                'prix': 150000.00,
                'stock': 2,
                'image_exterieur': 'products/sport/bmw serie 8/exterior.avif',
                'image_interieur': 'products/sport/bmw serie 8/interior.webp',
                'category_slug': 'sport'
            },
            {
                'nom': 'Nissan GT-R',
                'marque': 'Nissan',
                'modele': 2023,
                'transmission': 'Automatique',
                'description': 'Supercar légendaire alliant technologie de pointe et performances extrêmes.',
                'prix': 115000.00,
                'stock': 2,
                'image_exterieur': 'products/sport/nissan_gtr/exterior.webp',
                'image_interieur': 'products/sport/nissan_gtr/interior.webp',
                'category_slug': 'sport'
            },
            {
                'nom': 'Ford Shelby GT500',
                'marque': 'Ford',
                'modele': 2022,
                'transmission': 'Manuelle',
                'description': 'Muscle car américaine emblématique avec un V8 surpuissant.',
                'prix': 95000.00,
                'stock': 1,
                'image_exterieur': 'products/sport/ford shelby/exterior.jpeg',
                'image_interieur': 'products/sport/ford shelby/interior.jpg',
                'category_slug': 'sport'
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