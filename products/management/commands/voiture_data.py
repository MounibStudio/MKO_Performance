# Chemin : ton_app/management/commands/populate_voitures.py
#
# Structure des images attendue :
#   media/products/{CATEGORIE}/{Nom Voiture Année}/exterieur.jpg
#   media/products/{CATEGORIE}/{Nom Voiture Année}/interieur.jpg
#
# Pour modifier un chemin d'image, cherche la voiture dans VOITURES_DATA
# et change "image_exterieur" et "image_interieur"

from django.core.management.base import BaseCommand
from products.models import Category, Voiture
from django.utils.text import slugify


VOITURES_DATA = [

# ─── CONVERTIBLE AUTOMATIQUE ─────────────────────────
{
    "category": "CONVERTIBLE AUTOMATIQUE",
    "nom": "Audi A5 Cabriolet",
    "marque": "Audi",
    "modele": 2021,
    "transmission": "Automatique",
    "description": "Cabriolet Audi élégant.",
    "prix": 900.00,
    "stock": 1,
    "image_exterieur": "products/CONVERTIBLE AUTOMATIQUE/Audi A5 Cabriolet 2021/audi_ext.avif",
    "image_interieur": "products/CONVERTIBLE AUTOMATIQUE/Audi A5 Cabriolet 2021/audi_int.jpg",
},
{
    "category": "CONVERTIBLE AUTOMATIQUE",
    "nom": "BMW M4 Cabriolet",
    "marque": "BMW",
    "modele": 2021,
    "transmission": "Automatique",
    "description": "Cabriolet BMW sportif.",
    "prix": 1200.00,
    "stock": 1,
    "image_exterieur": "media/products/CONVERTIBLE AUTOMATIQUE/BMW M4 CABRIOLET 2021/m4_ext.avif",
    "image_interieur": "media/products/CONVERTIBLE AUTOMATIQUE/BMW M4 CABRIOLET 2021/m4_int.jpg",
},
{
    "category": "CONVERTIBLE AUTOMATIQUE",
    "nom": "Mercedes CLE 450",
    "marque": "Mercedes-Benz",
    "modele": 2026,
    "transmission": "Automatique",
    "description": "Cabriolet Mercedes haut de gamme.",
    "prix": 1400.00,
    "stock": 1,
    "image_exterieur": "products/CONVERTIBLE AUTOMATIQUE/New 2026 Mercedes-Benz CLE CLE 450/mercedes_ext.webp",
    "image_interieur": "products/CONVERTIBLE AUTOMATIQUE/New 2026 Mercedes-Benz CLE CLE 450/mercedes_int.jpg",
},

# ─── COUPE ─────────────────────────
{
    "category": "COUPE",
    "nom": "Audi A5 Coupe",
    "marque": "Audi",
    "modele": 2022,
    "transmission": "Automatique",
    "description": "Coupé Audi.",
    "prix": 650.00,
    "stock": 1,
    "image_exterieur": "products/Coupe/audi/exterior.jpg",
    "image_interieur": "products/Coupe/audi/interior.jpg",
},
{
    "category": "COUPE",
    "nom": "BMW Serie 4 Coupe",
    "marque": "BMW",
    "modele": 2022,
    "transmission": "Automatique",
    "description": "Coupé BMW.",
    "prix": 700.00,
    "stock": 1,
    "image_exterieur": "products/Coupe/bmw/exterior.jpg",
    "image_interieur": "products/Coupe/bmw/interior.jpg",
},
{
    "category": "COUPE",
    "nom": "Mercedes C-Class Coupe",
    "marque": "Mercedes-Benz",
    "modele": 2022,
    "transmission": "Automatique",
    "description": "Coupé Mercedes.",
    "prix": 750.00,
    "stock": 1,
    "image_exterieur": "products/Coupe/mercedes/exterior.jpg",
    "image_interieur": "products/Coupe/mercedes/interior.jpg",
},

# ─── LIMOUSINE ─────────────────────────
{
    "category": "LIMOUSINE",
    "nom": "Hummer Limousine",
    "marque": "Hummer",
    "modele": 2011,
    "transmission": "Automatique",
    "description": "Limousine Hummer luxueuse.",
    "prix": 2500.00,
    "stock": 1,
    "image_exterieur": "products/Hummer Limousine Service 2011/white-hummer-strech-limo.png",
    "image_interieur": "products/Hummer Limousine Service 2011/San-Diego-hummer-h2-limousine-interior.jpg",
},


# ─── HOT HATCH ─────────────────────────
{
    "category": "HOT HATCH",
    "nom": "Hyundai i30",
    "marque": "Hyundai",
    "modele": 2021,
    "transmission": "Automatique",
    "description": "Compacte Hyundai.",
    "prix": 400.00,
    "stock": 1,
    "image_exterieur": "products/Hot hatch AUTOMATIQUE/2021 Hyundai i30 hatch/hyundai_ext.webp",
    "image_interieur": "products/Hot hatch AUTOMATIQUE/2021 Hyundai i30 hatch/hyundai_int.avif",
},
{
    "category": "HOT HATCH",
    "nom": "Volkswagen Golf R",
    "marque": "Volkswagen",
    "modele": 2026,
    "transmission": "Automatique",
    "description": "Golf sportive.",
    "prix": 650.00,
    "stock": 1,
    "image_exterieur": "products/Hot hatch AUTOMATIQUE/2026 Volkswagen Golf R 2.0T/golf_ext.avif",
    "image_interieur": "products/Hot hatch AUTOMATIQUE/2026 Volkswagen Golf R 2.0T/golf_int.jpg",
},
{
    "category": "HOT HATCH",
    "nom": "Opel Corsa",
    "marque": "Opel",
    "modele": 2019,
    "transmission": "Automatique",
    "description": "Citadine Opel.",
    "prix": 300.00,
    "stock": 1,
    "image_exterieur": "products/Hot hatch AUTOMATIQUE/Opel  2019/opel-2019-20-corsa-e.jpg",
    "image_interieur": "products/Hot hatch AUTOMATIQUE/Opel  2019/Opel-Corsa-40-2022-ER-36.jpg",
},
{
    "category": "HOT HATCH",
    "nom": "Peugeot 208",
    "marque": "Peugeot",
    "modele": 2025,
    "transmission": "Automatique",
    "description": "Peugeot moderne.",
    "prix": 350.00,
    "stock": 1,
    "image_exterieur": "products/Hot hatch AUTOMATIQUE/PEUGEOT New 208 2025/peugot_ext.png",
    "image_interieur": "products/Hot hatch AUTOMATIQUE/PEUGEOT New 208 2025/peugot_int.webp",
},
{
    "category": "HOT HATCH",
    "nom": "Renault Megane GT",
    "marque": "Renault",
    "modele": 2022,
    "transmission": "Automatique",
    "description": "Megane sportive.",
    "prix": 450.00,
    "stock": 1,
    "image_exterieur": "products/Hot hatch AUTOMATIQUE/RENAULT , Renault, Megane, Estate, GT Line/renault_ext.jpg",
    "image_interieur": "products/Hot hatch AUTOMATIQUE/RENAULT , Renault, Megane, Estate, GT Line/renault_int.jpg",
},

# ─── PICKUP ─────────────────────────
{
    "category": "PICKUP",
    "nom": "Toyota Tacoma",
    "marque": "Toyota",
    "modele": 2024,
    "transmission": "Automatique",
    "description": "Pickup Toyota.",
    "prix": 750.00,
    "stock": 1,
    "image_exterieur": "products/Pickup truck AUTOMATIQUE/2024 Toyota Tacoma Interior/Toyota-Tacoma.avif",
    "image_interieur": "products/Pickup truck AUTOMATIQUE/2024 Toyota Tacoma Interior/int1.jpg",
},
{
    "category": "PICKUP",
    "nom": "Volkswagen Amarok",
    "marque": "Volkswagen",
    "modele": 2014,
    "transmission": "Automatique",
    "description": "Pickup Amarok.",
    "prix": 650.00,
    "stock": 1,
    "image_exterieur": "products/Pickup truck AUTOMATIQUE/Amarok  4X4 Ute  Volkswagen 2014/amarok_exterior.jpg",
    "image_interieur": "products/Pickup truck AUTOMATIQUE/Amarok  4X4 Ute  Volkswagen 2014/amarok_interior.jpg",
},
{
    "category": "PICKUP",
    "nom": "Ford Raptor",
    "marque": "Ford",
    "modele": 2018,
    "transmission": "Automatique",
    "description": "Pickup Ford Raptor.",
    "prix": 900.00,
    "stock": 1,
    "image_exterieur": "products/Pickup truck AUTOMATIQUE/FORD raptor 2018/(photo-sp)-1562340549.jpg",
    "image_interieur": "products/Pickup truck AUTOMATIQUE/FORD raptor 2018/ford_raptor_exterior.png",
},


# ─── SEDANS ─────────────────────────
{
    "category": "SEDANS",
    "nom": "Audi A6",
    "marque": "Audi",
    "modele": 2022,
    "transmission": "Automatique",
    "description": "Berline Audi.",
    "prix": 650.00,
    "stock": 1,
    "image_exterieur": "products/Sedans/audi/exterior.jpg",
    "image_interieur": "products/Sedans/audi/interior.jpg",
},
{
    "category": "SEDANS",
    "nom": "BMW Serie 5",
    "marque": "BMW",
    "modele": 2022,
    "transmission": "Automatique",
    "description": "Berline BMW.",
    "prix": 700.00,
    "stock": 1,
    "image_exterieur": "products/Sedans/bmw/exterior.jpg",
    "image_interieur": "products/Sedans/bmw/interior.jpg",
},
{
    "category": "SEDANS",
    "nom": "Mercedes C-Class Sedans",
    "marque": "Mercedes-Benz",
    "modele": 2022,
    "transmission": "Automatique",
    "description": "Berline Mercedes.",
    "prix": 750.00,
    "stock": 1,
    "image_exterieur": "products/Sedans/mercedes/exterior.jpg",
    "image_interieur": "products/Sedans/mercedes/interior.jpg",
},


# ─── SPORT ─────────────────────────
{
    "category": "SPORT",
    "nom": "BMW Série 8",
    "marque": "BMW",
    "modele": 2022,
    "transmission": "Automatique",
    "description": "Coupé BMW Série 8 haut de gamme.",
    "prix": 1600.00,
    "stock": 1,
    "image_exterieur": "products/sport/bmw serie 8/exterior.avif",
    "image_interieur": "products/sport/bmw serie 8/interior.webp",
},
{
    "category": "SPORT",
    "nom": "Ford Shelby",
    "marque": "Ford",
    "modele": 2022,
    "transmission": "Manuelle",
    "description": "Muscle car Shelby.",
    "prix": 1500.00,
    "stock": 1,
    "image_exterieur": "products/sport/ford shelby/exterior.jpeg",
    "image_interieur": "products/sport/ford shelby/interior.jpg",
},
{
    "category": "SPORT",
    "nom": "Nissan GTR 35",
    "marque": "Nissan",
    "modele": 2022,
    "transmission": "Automatique",
    "description": "Supercar japonaise iconique.",
    "prix": 2000.00,
    "stock": 1,
    "image_exterieur": "products/sport/nissan_gtr/exterior.webp",
    "image_interieur": "products/sport/nissan_gtr/interior.webp",
},



# ─── SUV ─────────────────────────
{
    "category": "SUV",
    "nom": "Audi Q8",
    "marque": "Audi",
    "modele": 2022,
    "transmission": "Automatique",
    "description": "SUV Audi.",
    "prix": 900.00,
    "stock": 1,
    "image_exterieur": "products/SUV/audi/exterior.jpg",
    "image_interieur": "products/SUV/audi/interiro.jpg",
},
{
    "category": "SUV",
    "nom": "BMW X5",
    "marque": "BMW",
    "modele": 2022,
    "transmission": "Automatique",
    "description": "SUV BMW.",
    "prix": 1000.00,
    "stock": 1,
    "image_exterieur": "products/SUV/bmw/exteriror.webp",
    "image_interieur": "products/SUV/bmw/interior.webp",
},
{
    "category": "SUV",
    "nom": "Mercedes-Benz GLC",
    "marque": "Mercedes-Benz",
    "modele": 2022,
    "transmission": "Automatique",
    "description": "SUV Mercedes.",
    "prix": 1100.00,
    "stock": 1,
    "image_exterieur": "products/SUV/mercedes/exteriro.webp",
    "image_interieur": "products/SUV/mercedes/interiro.webp",
},
{
    "category": "SUV",
    "nom": "Range Rover Sport",
    "marque": "Land Rover",
    "modele": 2020,
    "transmission": "Automatique",
    "description": "SUV luxe.",
    "prix": 1800.00,
    "stock": 1,
    "image_exterieur": "products/SUV/Range rover 2020/exterior.png",
    "image_interieur": "products/SUV/Range rover 2020/interior.webp",
},
{
    "category": "SUV",
    "nom": "Volkswagen Touareg",
    "marque": "Volkswagen",
    "modele": 2023,
    "transmission": "Automatique",
    "description": "SUV premium Volkswagen avec design élégant, moteur puissant et technologies avancées d’aide à la conduite.",
    "prix": 1200.00,
    "stock": 2,
    "image_exterieur": "products/SUV/Volkswagen/exteriro.jpg",
    "image_interieur": "products/SUV/Volkswagen/interiro.webp",
}


]


class Command(BaseCommand):
    help = "Remplit la base de données avec 25 voitures complètes (images incluses)"

    def handle(self, *args, **kwargs):

        created_count = 0

        for data in VOITURES_DATA:
            # Créer ou récupérer la catégorie
            category_nom = data["category"]
            slug = slugify(category_nom)
            category, _ = Category.objects.get_or_create(
                nom=category_nom,
                defaults={"slug": slug}
            )

            # Créer la voiture avec ses images
            Voiture.objects.update_or_create(
                nom=data["nom"],
                modele=data["modele"],
                defaults={
                    "marque": data["marque"],
                    "transmission": data["transmission"],
                    "description": data["description"],
                    "prix": data["prix"],
                    "stock": data["stock"],
                    "image_exterieur": data["image_exterieur"],
                    "image_interieur": data["image_interieur"],
                    "category": category,
                }
            )
            created_count += 1
