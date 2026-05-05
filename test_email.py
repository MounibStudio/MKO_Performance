#!/usr/bin/env python
import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
sys.path.insert(0, '/home/mounib/Documents/Projects/MKO_Performance')
django.setup()

from django.conf import settings
from django.core.mail import send_mail

print("=== Test envoi email ===")
print(f"EMAIL_HOST: {settings.EMAIL_HOST}")
print(f"EMAIL_PORT: {settings.EMAIL_PORT}")
print(f"EMAIL_HOST_USER: {settings.EMAIL_HOST_USER}")
print(f"DEFAULT_FROM_EMAIL: {settings.DEFAULT_FROM_EMAIL}")
print(f"EMAIL_HOST_PASSWORD: {settings.EMAIL_HOST_PASSWORD[:5]}..." if settings.EMAIL_HOST_PASSWORD else "EMAIL_HOST_PASSWORD: None")
print()

try:
    result = send_mail(
        'Test MKO Performance',
        'Test email - si tu reçois ce message, l\'email fonctionne!',
        settings.DEFAULT_FROM_EMAIL,
        [settings.EMAIL_HOST_USER],
        fail_silently=False,
    )
    print(f"✅ Email envoyé! Résultat: {result}")
except Exception as e:
    print(f"❌ Erreur: {type(e).__name__}: {e}")