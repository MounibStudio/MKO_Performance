from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from base.views import chatbot_api

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('base.urls')),
    path('voitures/', include('products.urls')),
    path('accounts/', include('users.urls')),
    path('panier/', include('cart.urls', namespace='cart')),
    path('api/chatbot/', chatbot_api, name='chatbot_api'),
    path("emails/", include("emails.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)