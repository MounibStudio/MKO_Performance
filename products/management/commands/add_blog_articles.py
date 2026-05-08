from django.core.management.base import BaseCommand
from products.models import Article
from django.core.files import File
from pathlib import Path

class Command(BaseCommand):
    help = 'Crée des articles de blog'

    def handle(self, *args, **options):
        base_dir = Path(__file__).resolve().parent.parent.parent.parent
        media_blog_path = base_dir / 'media' / 'blog'

        articles = [
            {
                'titre': 'Les tendances automobiles 2026',
                'slug': 'tendances-automobiles-2026',
                'contenu': '''Le marché automobile marocain connaît une évolution rapide en 2026. Les tendances principales sont:

1. L'électrique en hausse - De plus en plus de clients optent pour des véhicules hybrides et électriques
2. Les SUV dominent - Les véhicules familiaux et les 4x4 restent très demandés
3. La connectivité - Les nouvelles voitures sont de plus en plus connectées
4. Le partage - La location de courte durée gagne en popularité

Chez MKO Performance, nous adaptons notre flotte pour répondre à ces nouvelles attentes.''',
                'image': 'blog1.png',
            },
            {
                'titre': 'Guide: Bien choisir sa voiture de location',
                'slug': 'guide-choisir-voiture-location',
                'contenu': '''Choisir le bon véhicule pour votre location au Maroc peut faire toute la différence. Voici nos conseils:

1. Définissez vos besoins - Voyage en famille, business ou leisure?
2. Vérifiez les inclus -Kilométrage, assurance, assistance
3. Comparez les tarifs - Le prix le plus bas n est pas toujours le meilleur
4. Lisez les avis - Les retours clients sont précieux

Notre équipe est là pour vous guider vers le véhicule idéal.''',
                'image': 'blog2.png',
            },
            {
                'titre': 'MKO Performance: Notre engagement qualité',
                'slug': 'engagement-qualite-mko',
                'contenu': '''Depuis notre création, MKO Performance s engage à offrir le meilleur service:

✓ Flotte récente et entretenue
✓ Service client disponible 7j/7
✓ Tarifs transparents sans frais cachés
✓ Processus de réservation simple et rapide
✓ Support WhatsApp pour répondres à vos questions

La satisfaction de nos clients est notre priorité absolue.''',
                'image': 'blog3.png',
            },
        ]

        for article_data in articles:
            image_name = article_data.pop('image', None)
            article, created = Article.objects.get_or_create(
                slug=article_data['slug'],
                defaults=article_data
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'Article créé: {article.titre}'))
            else:
                self.stdout.write(f'Article existant: {article.titre}')
            
            if image_name and not article.image:
                image_path = media_blog_path / image_name
                if image_path.exists():
                    with open(image_path, 'rb') as f:
                        article.image.save(image_name, File(f), save=True)
                    self.stdout.write(self.style.SUCCESS(f'  Image added: {image_name}'))
                else:
                    self.stdout.write(self.style.WARNING(f'  Image not found: {image_path}'))

        self.stdout.write(self.style.SUCCESS('Terminé!'))