from django.shortcuts import render
import requests
from dotenv import load_dotenv
import os
from django.http import JsonResponse
from rest_framework import generics
from rest_framework.views import APIView 
from rest_framework.permissions import AllowAny, IsAuthenticated
from .models import *
from .serializers import *

load_dotenv()
api = os.getenv("WEATHER_API")

class RegisterUserView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        user = serializer.save()
        user.set_password(self.request.data['password'])
        user.save()
        return user
    
def get_forecast_view(request):

    location = request.GET.get("location")
    api_key = api
    
    if not location:
        return JsonResponse({"Error debes proporcionar una ubicacion"}, status=400)

    url = f"https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/{location}?key={api_key}"
    response = requests.get(url)
    
    if response.status_code == 200:
        clima_respuesta = response.json()
        return JsonResponse(clima_respuesta)
    else:
        print('Error', response.status_code, response.text)

