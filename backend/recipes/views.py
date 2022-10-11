from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponse, FileResponse

from io import BytesIO
from django.core.files.base import ContentFile

from .models import Recipe, RecipeIngredient, ShoppingCart


@login_required
@user_passes_test(lambda u: u.is_staff, login_url='/')
def shopping_cart(request, pk):
    instances = ShoppingCart.objects.filter(author_id=pk)
    shopping_list = []
    for instance in instances:
        recipe = Recipe.objects.get(name=instance.recipe)
        recipe_ingredients = RecipeIngredient.objects.filter(recipe=recipe)
        for ingredient in recipe_ingredients:
            shopping_list.append(
                f"{ingredient.recipe}: {ingredient.ingredient.name}"
                f" - {ingredient.amount}"
            )
    # f = open("shopping_cart{}.txt".format(pk), "w")
    # for shopping in shopping_list:
    #     f.write(shopping)
    # f.close()

    # # generate dynamic file content using object pk
    
    # # return HttpResponse(shopping_list, content_type="text/plain")
    # return response
    # output_file = io.BytesIO()
    # f = open("shopping_cart.txt", "w")
    # for shopping in shopping_list:
    #     f.write(shopping)
    # f.close()
    # with open("shopping_cart.txt", "w") as f:
    #     for shopping in shopping_list:
    #         f.write(shopping)
    #     f.seek(0)
    #     response = FileResponse(f, content_type='application/force-download')
    #     response['Content-Disposition'] = (
    #         'attachment; filename="shopping_cart.txt"'
    #     )
    #     return response

    # return HttpResponse(shopping_list, content_type="text/plain")
    # f = open("shopping_cart.txt", "wb")
    # for shopping in shopping_list:
    #     f.write(shopping.encode("UTF-8"))
    # f.close()
    # return HttpResponse(f.read(), content_type="text/plain")
    print(shopping_list)
    f = ContentFile('/n'.join(shopping_list))
    response = FileResponse(f.read(), content_type="text/plain")
    response['Content-Disposition'] = 'attachment; filename=%s' % 'shopping_cart.txt'
    return response
