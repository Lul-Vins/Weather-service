import requests
from dotenv import load_dotenv
import os
from django.http import JsonResponse

load_dotenv()

api = os.getenv("WEATHER_API")

def get_forecast_view(request):

    location = request.GET.get("location")
    api_key = api
    
    if not location:
        return JsonResponse({"Error debes proporcionar una ubicacion"}, status=400)

    url = f"https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/{location}?key={api_key}"
    response = requests.get(url)
    
    if response.status_code == 200:
        clima_respuesta = response.json()
        return clima_respuesta
    else:
        print('Error', response.status_code, response.text)

