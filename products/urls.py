from django.urls import path
from .views import ProductListView, VoitureDetailView

urlpatterns = [
    path('', ProductListView.as_view(), name='product_list'),
    path('<int:pk>/', VoitureDetailView.as_view(), name='voiture_detail'),
]