from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import User
import re
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'password']
        extra_kwargs = {
            'password' : {'write_only': True, 'min_length': 8}

        }
    def validate_password(self, value):
        if not any(char.isupper() for char in value):
            raise serializers.ValidationError("La contraseña debe tener al menos una letra Mayuscula")
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', value):
            raise serializers.ValidationError("La contraseña debe contener al menos un caracter especial")
        return value
    
    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Este correo ya esta registrado, intento con otro")
        return value
    
    def create(self, validated_data):
        password = validated_data.pop('password', None)
        if not password:
            raise serializers.ValidationError({"password": "Este campo es obligatorio"})
        
        user = User(**validated_data)

        if password:
            user.set_password(password)
        user.save()
        return user
        
        
        