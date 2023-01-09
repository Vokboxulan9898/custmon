from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import User
from django.contrib.auth import authenticate
User = get_user_model()

class RegistrationSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(min_length=4, required=True)
    password_confirm = serializers.CharField(min_length=4, required=True)

    name = serializers.CharField(max_length=15, required=True)
    last_name = serializers.CharField(max_length=40, required=True)

    def validate_email(self, email):
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError('Ползователь с таким еmail уже сушествует')
        return email

    def validate(self, attr):
        password = attr.get('password')
        password2 = attr.pop('password_confirm')
        if password != password2:
            raise serializers.ValidationError('Пароли не совподают')
        return attr


    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password =serializers.CharField(required=True)

    def validate_email(self, email):
        if not User.objects.filter(email=email).exists():
            raise serializers.ValidationError('Пользователь не найден')
        return email

    def validate(self, data):
        request = self.context.get('request')
        email = data.get('email')
        password = data.get('password')
        if email and password:
            user = authenticate(username=email, password=password, requset=request)
            if not user:
                raise serializers.ValidationError('неверный email или пароль')
        else:
            raise serializers.ValidationError('email и пароль обязательны к заполнению')
        data['user'] = user
        return data
