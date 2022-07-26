from django.contrib import admin

from recipes.models import (
    Favorite,
    Ingredient,
    Recipe,
    RecipeIngredient,
    Tag
)


class TagAdmin(admin.ModelAdmin):
    list_display = ("slug", "name", "color")


class IngredientAdmin(admin.ModelAdmin):
    list_display = ("name", "measurement_unit")
    list_filter = ("name",)


class RecipeAdmin(admin.ModelAdmin):
    list_display = ("author", "name", "favorites")
    search_fields = ("text",)
    list_filter = ("author", "name", "tags")

    def favorites(self, obj):
        fav = Favorite.objects.filter(recipe=obj)
        return fav.count()


class RecipeIngredienAdmin(admin.ModelAdmin):
    list_display = ("recipe", "ingredient", "amount")


class FavoriteAdmin(admin.ModelAdmin):
    list_display = ("author", "recipe")


admin.site.register(Tag, TagAdmin)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(RecipeIngredient, RecipeIngredienAdmin)
admin.site.register(Favorite, FavoriteAdmin)
