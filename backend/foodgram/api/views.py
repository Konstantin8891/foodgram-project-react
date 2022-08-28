import email

from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination
from rest_framework import parsers, renderers
from rest_framework.authtoken.models import Token
from rest_framework.viewsets import ReadOnlyModelViewSet, ModelViewSet
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly

from .serializers import (
    FollowSerializer, RecipeViewSerializer, RecipeWriteSerializer, ShortRecipeSerializer, TagSerializer, UserSerializer, AuthCustomTokenSerializer,
    IngredientSerializer, 
    ShoppingCartCreateSerializer, RecipeWriteSerializer
)
from users.models import User
from recipes.models import Recipe, Subscriber, Tag, Ingredient, ShoppingCart, RecipeIngredient, Favorite, Subscriber
from .mixins import CreateListRetrieveViewSet, CreateViewSet, DestroyViewSet
from .permissions import IsAuthorOrReadOnly


class UserListViewSet(CreateListRetrieveViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    pagination_class = PageNumberPagination
    lookup_field = 'id'


class CurrentUser(generics.RetrieveAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())
        obj = queryset.get(pk=self.request.user.id)
        self.check_object_permissions(self.request, obj)
        return obj


class SetPasswordAPIView(APIView):
    def post(self, request):
        if request.user.is_anonymous:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        try:
            data = request.data['current_password']
        except:
            return Response(data={'current_password': ["Обязательное поле."]}, status=status.HTTP_400_BAD_REQUEST)
        try:
            data = request.data['new_password']
        except:
            return Response(data={'new_password': ["Обязательное поле."]}, status=status.HTTP_400_BAD_REQUEST)
        if request.user.password != request.data['current_password']:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        user = User.objects.get(username=request.user.username)
        serializer = UserSerializer(user, data={'password': request.data['new_password']}, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ObtainAuthToken(APIView):
    throttle_classes = ()
    permission_classes = ()
    parser_classes = (
        parsers.FormParser,
        parsers.MultiPartParser,
        parsers.JSONParser,
    )
    renderer_classes = (renderers.JSONRenderer,)

    def post(self, request):
        serializer = AuthCustomTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']
        user = User.objects.get(email=email)
        token, created = Token.objects.get_or_create(user=user)
        content = {
            'token': token.key,
        }

        return Response(content)
    

class DeleteToken(APIView):

    def post(self, request):
        try:
            instance = self.request.headers['authorization']
            instance = instance[6:]
            instance = Token.objects.get(key=instance).delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except:
            return Response(status=status.HTTP_401_UNAUTHORIZED)


class TagViewSet(ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class IngredientViewSet(ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer


class RecipeViewSet(ModelViewSet):
    queryset = Recipe.objects.all()
    permission_classes = [IsAuthorOrReadOnly]

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return RecipeViewSerializer
        return RecipeWriteSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True, context={'request': request})
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True, context={'request': request})
        return Response(serializer.data)

    def create_instance(self, author, recipe_id, model):
        obj, created = model.objects.get_or_create(
            author=author, recipe_id=recipe_id
        )
        if not created:
            raise ValidationError(
                f'{model.__class__.__name__} already exists'
            )
        serializer_obj = Recipe.objects.get(pk=recipe_id)
        serializer = ShortRecipeSerializer(instance=serializer_obj)
        return Response(
            data=serializer.data,
            status=status.HTTP_201_CREATED,
        )

    def delete_instance(self, author, recipe_id, model):
        model.objects.get(author=author, recipe_id=recipe_id).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=['POST', 'DELETE'], permission_classes=[IsAuthenticated])
    def shopping_cart(self, request, pk):
        if request.method == 'POST':
            try:
                ShoppingCart.objects.get(recipe_id=pk, author=request.user)
                return Response(data='Рецепт уже добавлен в список покупок', status=status.HTTP_400_BAD_REQUEST)
            except:
                return self.create_instance(
                    author=request.user, recipe_id=pk, model=ShoppingCart
                )
        if request.method == 'DELETE':
            try:
                return self.delete_instance(
                    request.user, pk, ShoppingCart
                )
            except:
                return Response(data='рецепта в списке покупок нет', status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['GET', ], permission_classes=[IsAuthenticated])
    def download_shopping_cart(self, request):
        instances = ShoppingCart.objects.filter(author=request.user)
        shopping_list = []
        for instance in instances:
            recipe = Recipe.objects.get(name=instance.recipe)
            recipe_ingredients = RecipeIngredient.objects.filter(recipe=recipe)
            for ingredient in recipe_ingredients:
                shopping_list.append(
                    f'{ingredient.recipe}: {ingredient.ingredient}'
                    f' - {ingredient.amount}\n'
                )
        f = open('shopping_cart.txt', 'w')
        for shopping in shopping_list:
            f.write(shopping)
        
        response = HttpResponse(shopping_list, content_type='text/plain')
        f.close()
        return response


    @action(detail=True, methods=['POST', 'DELETE'], permission_classes=[IsAuthenticated])
    def favorite(self, request, pk):
        if request.method == 'POST':
            try:
                Favorite.objects.get(recipe_id=pk, author=request.user)
                return Response(data='Рецепт уже добавлен в избранное', status=status.HTTP_400_BAD_REQUEST)
            except:
                return self.create_instance(
                    author=request.user, recipe_id=pk, model=Favorite
                )
        if request.method == 'DELETE':
            try:
                return self.delete_instance(
                    request.user, pk, Favorite
                )
            except:
                return Response(data='рецепта в избранном нет', status=status.HTTP_400_BAD_REQUEST)


class CreateDestroyFollowerAPIView(APIView):
    def post(self, request, id):
        author = User.objects.get(id=id)
        Subscriber.objects.get_or_create(
            author=author, user=request.user
        )
        author = User.objects.get(id=self.request.user.id)
        # print(self.request.user.id)
        context = {'request': request}
        serializer = FollowSerializer(instance=author, context=context)
        # serializer.is_valid()
        # print(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def delete(self, request, id):
        author = User.objects.get(id=id)
        try:
            Subscriber.objects.get(author=author, user=request.user).delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)
