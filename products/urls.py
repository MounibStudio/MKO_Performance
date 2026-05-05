from django.urls import path
from .views import ProductListView, VoitureDetailView, ajouter_review, BlogListView, BlogDetailView

urlpatterns = [
    path('', ProductListView.as_view(), name='product_list'),
    path('<int:pk>/', VoitureDetailView.as_view(), name='voiture_detail'),
    path('<int:voiture_id>/review/', ajouter_review, name='ajouter_review'),
    path('blog/', BlogListView.as_view(), name='blog_list'),
    path('blog/<slug:slug>/', BlogDetailView.as_view(), name='blog_detail'),
]