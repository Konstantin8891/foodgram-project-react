from django.contrib import admin
from recipes.models import (Favorite, Ingredient, Recipe, RecipeIngredient,
                            ShoppingCart, Tag)


class TagAdmin(admin.ModelAdmin):
    list_display = ("slug", "name", "color")

    class Meta:
        verbose_name_plural = "Тэги"


class IngredientAdmin(admin.ModelAdmin):
    list_display = ("name", "measurement_unit")
    list_filter = ("name",)

    class Meta:
        verbose_name_plural = "Ингредиенты"


class RecipeAdmin(admin.ModelAdmin):
    list_display = ("author", "name", "favorites")
    search_fields = ("text",)
    list_filter = ("author", "name", "tags")

    def favorites(self, obj):
        fav = Favorite.objects.filter(recipe=obj)
        return fav.count()

    class Meta:
        verbose_name_plural = "Рецепты"


class RecipeIngredienAdmin(admin.ModelAdmin):
    list_display = ("recipe", "ingredient", "amount")

    class Meta:
        verbose_name_plural = "Количество ингредиентов в рецепте"


class ShoppingCartAdmin(admin.ModelAdmin):
    list_display = ("author", "recipe")

    class Meta:
        verbose_name_plural = "Рецепт в списке покупок"


class FavoriteAdmin(admin.ModelAdmin):
    list_display = ("author", "recipe")

    class Meta:
        verbose_name_plural = "Избранное"


admin.site.register(Tag, TagAdmin)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(RecipeIngredient, RecipeIngredienAdmin)
admin.site.register(ShoppingCart, ShoppingCartAdmin)
admin.site.register(Favorite, FavoriteAdmin)
