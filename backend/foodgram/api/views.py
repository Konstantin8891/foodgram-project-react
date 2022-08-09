import email
from django.shortcuts import get_object_or_404
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination
from rest_framework import parsers, renderers
from rest_framework.authtoken.models import Token
from rest_framework.viewsets import ReadOnlyModelViewSet, ModelViewSet

from .serializers import TagSerializer, UserSerializer, AuthCustomTokenSerializer, IngredientSerializer, RecipeSerializer
from users.models import User
from recipes.models import Recipe, Tag, Ingredient
from .mixins import CreateListRetrieveViewSet

# @api_view(['GET', 'POST'])
# def users(request):
#     if request.method == 'POST':
#         serializer = UserSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#     users = User.objects.all()
#     serializer = UserSerializer(users, many=True)
#     return Response(serializer.data)
# class APIUsers(APIView):
#     def get(self, request):
#         users = User.objects.all()
#         serializer = UserSerializer(users, many=True)
#         return Response(serializer.data)

#     def post(self, request):
#         serializer = UserSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
# class UserList(generics.ListCreateAPIView):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer

class UserListViewSet(CreateListRetrieveViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    pagination_class = PageNumberPagination
    lookup_field = 'id'


# class UserDetail(generics.RetrieveAPIView):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer
#     lookup_field = 'id'


# @api_view(['GET'])
# def user_detail(request, user_id):
#     user = User.objects.filter(id=user_id)
#     serializer = UserSerializer(user, many=True)
#     return Response(serializer.data, status=status.HTTP_200_OK)

class CurrentUser(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    # lookup_field = 'id'

    # def get_queryset(self):
    #     # user_id = self.kwargs.get("user_id")
    #     user_id = self.request.user.id
    #     user = get_object_or_404(User, id=user_id)
    #     # new_queryset = get_list_or_404(Comment, post_id=post_id)
    #     # return new_queryset
    #     return user

    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())
        # make sure to catch 404's below
        obj = queryset.get(pk=self.request.user.id)
        self.check_object_permissions(self.request, obj)
        return obj


# @api_view(['GET', ])
# #@login_required
# def current_user(request):
#     user = User.objects.get(username=request.user.username)
#     serializer = UserSerializer(user)
#     return Response(serializer.data, status=status.HTTP_200_OK)


class SetPassword(generics.UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())
        # make sure to catch 404's below
        obj = queryset.get(pk=self.request.user.id)
        self.check_object_permissions(self.request, obj)
        return obj

    # def get_queryset(self):
    #     user_id = self.request.user.id
    #     new_queryset = User.objects.filter(id=user_id)
    #     return new_queryset

    def perform_update(self, serializer):
        # if self.request.data['current_password'] == self.request.user.password:
        #     # serializer = UserSerializer(user, data={'password': request.data['new_password']}, partial=True)
        #     serializer = UserSerializer(data={'password': self.request.data['new_password']}, partial=True)
        # if serializer.is_valid():
        # super(SetPassword, self).perform_update(serializer)
        serializer.save()

    def update(self, request, *args, **kwargs):
        # partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data={'password': request.data['new_password']}, partial=True)
        if request.data["current_password"] != request.user.password:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data, status=status.HTTP_204_NO_CONTENT)


    

# @api_view(['PATCH', ])
# # @login_required
# def set_password(request):
#     user = User.objects.get(username=request.user.username)
#     serializer = UserSerializer(user)
#     if request.data['current_password'] == request.user.password:
#         serializer = UserSerializer(user, data={'password': request.data['new_password']}, partial=True)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_204_NO_CONTENT)
#     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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
        # user = serializer.validated_data['user']
        # token, created = Token.objects.get_or_create(user=user)
        email = serializer.validated_data['email']
        user = User.objects.get(email=email)
        token, created = Token.objects.get_or_create(user=user)

        content = {
            # 'token': unicode(token.key),
            'token': token.key,
        }

        return Response(content)
    

class DeleteToken(generics.DestroyAPIView):
    queryset = Token.objects.all()
    serializer_class = AuthCustomTokenSerializer

    # def get_object(self):
    #     queryset = self.filter_queryset(self.get_queryset())
    #     # make sure to catch 404's below
    #     user = User.objects
    #     obj = queryset.get(email=self.request.user.email)
    #     self.check_object_permissions(self.request, obj)
    #     return obj

    def destroy(self, request, *args, **kwargs):
        instance = self.request.headers['authorization']
        instance = instance[6:]
        try:
            instance = Token.objects.get(key=instance)
            self.perform_destroy(instance)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except:
            return Response(status=status.HTTP_401_UNAUTHORIZED)


class TagViewSet(ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
# class ObtainAuthToken(CreateDestroyViewSet):
#     queryset = Token.objects.all()
#     serializer_class = AuthCustomTokenSerializer

#     def create(self, request, *args, **kwargs):
#         serializer = AuthCustomTokenSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         self.perform_create(serializer)
#         # user = serializer.validated_data['user']
#         # token, created = Token.objects.get_or_create(user=user)
#         email = serializer.validated_data['email']
#         user = User.objects.get(email=email)
#         token, created = Token.objects.get_or_create(user=user)

#         content = {
#             # 'token': unicode(token.key),
#             'token': token.key,
#         }

#         return Response(serializer, content, status=status.HTTP_201_CREATED)
    
#     def perform_create(self, serializer):
#         serializer.save()

class IngredientViewSet(ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer


class RecipeViewSet(ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)