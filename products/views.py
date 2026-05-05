from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib import messages
from django.http import JsonResponse
from django.db import models
from datetime import date, timedelta
from .models import Voiture, Category, Review, Article
from orders.models import ArticleCommande


class ProductListView(View):
    def get(self, request):
        today = date.today().isoformat()
        
        voitures = Voiture.objects.all().select_related('category')
        categories = Category.objects.all()

        prix_list = voitures.values_list('prix', flat=True)
        max_price = int(max(prix_list)) if prix_list else 5000

        return render(request, 'products/product_list.html', {
            'voitures': voitures,
            'categories': categories,
            'max_price': max_price,
            'today': today,
        })


class VoitureDetailView(View):
    def get(self, request, pk):
        today = date.today().isoformat()
        voiture = get_object_or_404(Voiture, pk=pk)

        similaires = Voiture.objects.filter(
            category=voiture.category
        ).exclude(pk=voiture.pk)[:3]
        
        blocked_dates = []
        today_date = date.today()
        reservations = ArticleCommande.objects.filter(
            voiture=voiture,
            commande__statut__in=['confirmee', 'en_attente']
        )
        for res in reservations:
            if res.date_debut and res.date_fin:
                current = res.date_debut.date() if hasattr(res.date_debut, 'date') else res.date_debut
                end = res.date_fin.date() if hasattr(res.date_fin, 'date') else res.date_fin
                while current <= end:
                    if current >= today_date:
                        blocked_dates.append(current.isoformat())
                    current += timedelta(days=1)

        reviews = Review.objects.filter(voiture=voiture)
        avg_note = reviews.aggregate(models.Avg('note'))['note__avg'] or 0
        
        return render(request, 'products/voiture_detail.html', {
            'voiture': voiture,
            'similaires': similaires,
            'today': today,
            'blocked_dates': blocked_dates,
            'reviews': reviews,
            'avg_note': round(avg_note, 1),
            'review_count': reviews.count(),
        })


@login_required
def ajouter_review(request, voiture_id):
    if request.method == 'POST':
        note = request.POST.get('note')
        commentaire = request.POST.get('commentaire')
        
        if not note or not commentaire:
            messages.error(request, "Veuillez remplir tous les champs.")
            return redirect('voiture_detail', pk=voiture_id)
        
        voiture = get_object_or_404(Voiture, pk=voiture_id)
        
        existing = Review.objects.filter(voiture=voiture, utilisateur=request.user).first()
        if existing:
            messages.warning(request, "Vous avez déjà noté cette voiture.")
            return redirect('voiture_detail', pk=voiture_id)
        
        Review.objects.create(
            voiture=voiture,
            utilisateur=request.user,
            note=int(note),
            commentaire=commentaire
        )
        
        messages.success(request, "Merci pour votre avis!")
        return redirect('voiture_detail', pk=voiture_id)
    
    return redirect('voiture_detail', pk=voiture_id)


class BlogListView(View):
    def get(self, request):
        articles = Article.objects.filter(statut='publie')
        return render(request, 'products/blog_list.html', {
            'articles': articles,
        })


class BlogDetailView(View):
    def get(self, request, slug):
        article = get_object_or_404(Article, slug=slug, statut='publie')
        recent = Article.objects.filter(statut='publie').exclude(pk=article.pk)[:3]
        return render(request, 'products/blog_detail.html', {
            'article': article,
            'recent_articles': recent,
        })