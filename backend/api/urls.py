from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views

app_name = 'api'

router = DefaultRouter()
router.register('users', views.UserViewSet, basename='users')
router.register('tags', views.TagViewSet, basename='tags')
router.register('ingredients', views.IngredientViewSet, basename='ingredients')
router.register('recipes', views.RecipeViewSet, basename='recipes')

urlpatterns = [
    # path('users/me/', views.CurrentUser.as_view(), name='current_user'),
    # path(
    #     'users/set_password/',
    #     views.SetPasswordAPIView.as_view(),
    #     name='set_password'
    # ),
    # path('users/<int:id>/subscribe/', views.CreateDestroyFollowerAPIView.as_view()),
    path('', include(router.urls)),
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
    # path('auth/token/login/', views.ObtainAuthToken.as_view()),
    # path('auth/token/logout/', views.DeleteToken.as_view())
]