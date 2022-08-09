from django.urls import path

from . import views

app_name = 'recipes'

urlpatterns = [
    path('', views.index, name='index'),
    path('recipe_create/', views.recipe_create, name='recipe_create'),
]