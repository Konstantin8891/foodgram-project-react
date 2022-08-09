import email

from django.shortcuts import get_object_or_404
from django.contrib.auth import authenticate
from rest_framework import serializers, exceptions

import webcolors

from recipes.models import Tag, Ingredient, Recipe
from users.models import User


class Hex2NameColor(serializers.Field):
    # При чтении данных ничего не меняем - просто возвращаем как есть
    def to_representation(self, value):
        return value
    # При записи код цвета конвертируется в его название
    def to_internal_value(self, data):
        # Доверяй, но проверяй
        try:
            # Если имя цвета существует, то конвертируем код в название
            data = webcolors.hex_to_name(data)
        except ValueError:
            # Иначе возвращаем ошибку
            raise serializers.ValidationError('Для этого цвета нет имени')
        # Возвращаем данные в новом формате
        return data


class TagSerializer(serializers.ModelSerializer):
    # recipes = serializers.StringRelatedField(many=True, read_only=True)
    color = Hex2NameColor()

    class Meta:
        model = Tag
        # fields = ('name', 'color', 'recipes')
        fields = ('name', 'color', 'slug')

    def __str__(self):
        return self.name


class IngredientSerializer(serializers.ModelSerializer):
    # recipes = serializers.StringRelatedField(many=True, read_only=True)

    class Meta:
        model = Ingredient
        # fields = ('name', 'amount', 'unit', 'recipes')
        fields = ('name', 'amount', 'measurement_unit')

    def __str__(self):
        return self.name


class RecipeSerializer(serializers.ModelSerializer):
    ingredients = IngredientSerializer(read_only=True, many=True)
    tags = TagSerializer(read_only=True, many=True)

    class Meta:
        model = Recipe
        fields = '__all__'

    def __str__(self):
        return self.name


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'username', 'last_name', 'email', 'password']


class AuthCustomTokenSerializer(serializers.Serializer):
    # email = serializers.CharField()
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, attrs):
        # email_or_username = attrs.get('email_or_username')
        email = attrs.get('email')
        password = attrs.get('password')

        # if email_or_username and password:
        if email and password:
            # Check if user sent email
            # if validateEmail(email_or_username):
            # if validateEmail(email):
            user_request = get_object_or_404(
                User,
                # email=email_or_username,
                email=email,
            )

            # email_or_username = user_request.username
            email = user_request.email

            # user = authenticate(username=email_or_username, password=password)
            user = authenticate(username=email, password=password)

            # if user:
            #     if not user.is_active:
            #         msg = ('User account is disabled.')
            #         raise exceptions.ValidationError(msg)
            # else:
            #     msg = ('Unable to log in with provided credentials.')
            #     raise exceptions.ValidationError(msg)
        else:
            msg = ('Must include "email" and "password"')
            raise exceptions.ValidationError(msg)

        attrs['user'] = user
        return attrs