from django.shortcuts import render
from django.views import View
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
import requests

class HomeView(View):
    def get(self, request):
        return render(request, 'base/home.html', {})


class AboutView(View):
    def get(self, request):
        return render(request, 'base/about.html', {})


@csrf_exempt
def chatbot_api(request):
    if request.method == 'POST':
        import json
        try:
            data = json.loads(request.body)
            user_message = data.get('message', '')
            
            if not user_message:
                return JsonResponse({'error': 'Message vide'})
            
            system_prompt = """Tu es l'assistant virtuel de MKO Performance, une société de location de voitures de luxe au Maroc. 
Tu dois répondre ONLY en français aux questions sur:
- Les véhicules disponibles (Ford Raptor, Mercedes, BMW, etc.)
- Les prix de location
- Les conditions de location (pièce d'identité, permis)
- Les services proposés
- Le contact et support
- La réservation

Sois précis, concis et professionnel. Si tu ne sais pas, dis-le."""

            url = "https://api.groq.com/openai/v1/chat/completions"
            headers = {
                "Authorization": f"Bearer {settings.GROQ_API_KEY}",
                "Content-Type": "application/json"
            }
            payload = {
                "model": "llama-3.3-70b-versatile",
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_message}
                ],
                "temperature": 0.7,
                "max_tokens": 500
            }
            
            response = requests.post(url, headers=headers, json=payload, timeout=30)
            
            if response.status_code == 200:
                result = response.json()
                bot_reply = result['choices'][0]['message']['content']
                return JsonResponse({'response': bot_reply})
            else:
                return JsonResponse({'error': 'Erreur API'}, status=500)
                
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    
    return JsonResponse({'error': 'Méthode non autorisée'}, status=405)