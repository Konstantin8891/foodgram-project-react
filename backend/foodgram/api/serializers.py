import email

from django.shortcuts import get_object_or_404
from django.contrib.auth import authenticate
from rest_framework import serializers, exceptions

import webcolors

from recipes.models import (
    ShoppingCart, Tag, Ingredient, Recipe, RecipeIngredient, Favorite
)
from users.models import User
from recipes.models import Subscriber
from .base64 import Base64ImageField
from .hex import Hex2NameColor


class TagSerializer(serializers.ModelSerializer):
    color = Hex2NameColor()

    class Meta:
        model = Tag
        fields = ('id', 'name', 'color', 'slug')

    def __str__(self):
        return self.name


class IngredientSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit')

    def __str__(self):
        return self.name


class RecipeIngredientSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(queryset=Ingredient.objects.all())

    class Meta:
        model = RecipeIngredient
        fields = ('id', 'amount')


class RecipeViewSerializer(serializers.ModelSerializer):
    ingredients = serializers.SerializerMethodField(read_only=True)
    tags = TagSerializer(read_only=True, many=True)
    is_favorite = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        fields = (
            'name',
            'image',
            'text',
            'ingredients',
            'tags',
            'cooking_time',
            'is_favorite',
            'is_in_shopping_cart'
        )

    def __str__(self):
        return self.name
    
    def get_ingredients(self, obj):
        ingredients = RecipeIngredient.objects.filter(recipe=obj)
        return RecipeIngredientSerializer(ingredients, many=True).data

    def get_is_favorite(self, obj):
        request = self.context.get('request')
        if request.user.is_anonymous:
            return 0
        elif Favorite.objects.filter(
            author=request.user,
            recipe=obj
        ).exists():
            return 1
        else:
            return 0
        

    def get_is_in_shopping_cart(self, obj):
        request = self.context.get('request')
        if request.user.is_anonymous:
            return 0
        elif ShoppingCart.objects.filter(
            author=request.user, recipe=obj
        ).exists():
            return 1
        else:
            return 0

class RecipeWriteSerializer(serializers.ModelSerializer):
    ingredients = RecipeIngredientSerializer(many=True)
    tags = serializers.PrimaryKeyRelatedField(many=True, queryset=Tag.objects.all())
    image = Base64ImageField(
        max_length=None, use_url=True,
    )
    class Meta:
        model = Recipe
        fields = (
            'name', 'image', 'text', 'ingredients', 'tags', 'cooking_time'
        )

    def __str__(self):
        return self.name

    def create(self, validated_data):
        tags = validated_data.pop('tags')
        temp_ingredients = validated_data.pop('ingredients')
        recipe = Recipe.objects.create(
            author=self.context.get('request').user,
            name=validated_data.pop('name'),
            image=validated_data.pop('image'),
            text=validated_data.pop('text'),
            cooking_time=validated_data.pop('cooking_time')
        )
        recipe.tags.set(tags)
        for ingredient in temp_ingredients:
            print(ingredient)
            ingredient_instance = ingredient['id']
            amount = ingredient['amount']
            RecipeIngredient.objects.create(
                recipe=recipe, ingredient=ingredient_instance, amount=amount
            )
        return recipe

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.image = validated_data.get('image', instance.image)
        instance.text = validated_data.get('text', instance.text)
        instance.cooking_time = validated_data.get(
            'cooking_time', instance.cooking_time
        )
        
        tags = validated_data.get('tags')
        if tags != None:
            instance.tags.clear()
            for tag in tags:
                instance.tags.add(tag)
        
        ingredients = validated_data.get('ingredients')
        if ingredients != None:
            RecipeIngredient.objects.filter(recipe=instance).all().delete()
            for ingredient in ingredients:
                ingredient_id = ingredient['id']
                amount = ingredient['amount']
                RecipeIngredient.objects.create(
                    recipe=instance, ingredient=ingredient_id, amount=amount
                )
            instance.save()
        return instance

    def to_representation(self, instance):
        return RecipeViewSerializer(instance, context=self.context).data


class ShortRecipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'username', 'last_name', 'email', 'password']


class AuthCustomTokenSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')
        if email and password:
            user_request = get_object_or_404(
                User,
                email=email,
            )
            email = user_request.email
            user = authenticate(username=email, password=password)
        else:
            msg = ('Must include "email" and "password"')
            raise exceptions.ValidationError(msg)
        attrs['user'] = user
        return attrs

 
class ShoppingCartCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShoppingCart
        fields = ('author', 'recipe')

    def to_representation(self, instance):
        print()
        return ShortRecipeSerializer(instance.recipe, context=self.context).data


class FollowSerializer(serializers.ModelSerializer):
    is_subscribed = serializers.SerializerMethodField()
    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()
    class Meta:
        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
            'recipes',
            'recipes_count'
        )
    
    def get_is_subscribed(self, obj):
        request = self.context.get('request')
        # print(self.context)
        return Subscriber.objects.filter(author=obj, user=request.user).exists()

    def get_recipes(self, obj):
        request = self.context.get('request')
        context = {'request': request}
        recipes = obj.recipes.filter(author=request.user)
        return RecipeViewSerializer(recipes, many=True, context=context).data

    def get_recipes_count(self, obj):
        request = self.context.get('request')
        return obj.recipes.filter(author=request.user).count()