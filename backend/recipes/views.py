from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

from .models import ShoppingCart, Recipe, RecipeIngredient


@login_required
def shopping_cart(obj, pk):
    instances = ShoppingCart.objects.filter(author=obj)
    shopping_list = []
    for instance in instances:
        recipe = Recipe.objects.get(name=instance.recipe)
        recipe_ingredients = RecipeIngredient.objects.filter(recipe=recipe)
        for ingredient in recipe_ingredients:
            shopping_list.append(
                f"{ingredient.recipe}: {ingredient.ingredient.name}"
                f" - {ingredient.amount}\n"
            )
    f = open("shopping_cart{}.txt".format(pk), "w")
    for shopping in shopping_list:
        f.write(shopping)
    f.close()
    response = HttpResponse(content_type='application/force-download')
    response['Content-Disposition'] = (
        'attachment; filename="shopping_cart.txt"'
    )
    # generate dynamic file content using object pk
    response.write(f)
    # return HttpResponse(shopping_list, content_type="text/plain")
    return response
