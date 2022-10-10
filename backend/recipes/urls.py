from django.urls import path

from recipes import views

app_name = 'recipes'

urlpatterns = [
    path(
        'shopping_cart/<int:pk>/',
        views.shopping_cart,
        name='shopping_cart'
    ),
]
