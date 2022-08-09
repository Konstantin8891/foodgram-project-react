from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views

# from .views import ObtainAuthToken, CurrentUser, SetPassword, DeleteToken

app_name = 'api'

router = DefaultRouter()
router.register('users', views.UserListViewSet)
router.register('tags', views.TagViewSet)
router.register('ingredients', views.IngredientViewSet)
router.register('recipes', views.RecipeViewSet)


urlpatterns = [
    path('users/me/', views.CurrentUser.as_view(), name='current_user'),
    path('users/set_password/', views.SetPassword.as_view(), name='set_password'),
    path('', include(router.urls)),
    path('auth/token/login/', views.ObtainAuthToken.as_view()),
    path('auth/token/logout/', views.DeleteToken.as_view())
]