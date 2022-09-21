from django_filters.rest_framework import FilterSet
import django_filters

from recipes.models import Ingredient


class IngredientSearchFilter(FilterSet):
    name = django_filters.CharFilter(lookup_expr='istartswith')

    class Meta:
        model = Ingredient
        fields = ('name',)