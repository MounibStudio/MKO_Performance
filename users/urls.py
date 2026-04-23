from django.urls import path
from .views import LoginView, SignupView, logout_view

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('signup/', SignupView.as_view(), name='signup'),
    path('logout/', logout_view, name='logout'),
]