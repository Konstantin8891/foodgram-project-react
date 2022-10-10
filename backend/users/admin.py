from django.contrib import admin
from django.contrib.auth.models import Group
from django.http import HttpResponse
from django.urls import reverse, path
from django.utils.html import format_html

from rest_framework.authtoken.models import TokenProxy as BaseToken

from users.models import Subscriber, User, ProxyToken
from recipes.models import Recipe, RecipeIngredient, ShoppingCart


class UserAdmin(admin.ModelAdmin):
    readonly_fields = ('shopping_cart',)
    list_display = (
        "id",
        "username",
        "first_name",
        "last_name",
        "email",
        "shopping_cart"
    )
    list_filter = ("first_name", "email")

    def get_urls(self):
        urls = super(UserAdmin, self).get_urls()
        urls += [
            path(
                r'download-file/(?P<pk>\d+)$',
                self.download_file,
                name='users_user_download-file'
            ),
        ]
        return urls

    # custom "field" that returns a link to the custom function
    def shopping_cart(self, obj):
        return format_html(
            '<a href="{}">Download file</a>',
            reverse('admin:users_user_download-file', args=[obj.pk])
        )
    # download_link.short_description = "Download file"

    # add custom view function that downloads the file
    # def download_file(self, request, pk):
    #     response = HttpResponse(content_type='application/force-download')
    #     response['Content-Disposition'] = (
    #         'attachment; filename="whatever.txt"'
    #     )
    #     # generate dynamic file content using object pk
    #     response.write('whatever content')
    #     return response

    def download_file(self, pk, obj):
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
        f = open("shopping_cart.txt", "w")
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

    # def shopping_cart(self, obj):
    #     return format_html(
    #         '<a href="{}" target="_blank">Download file</a>',
    #         reverse('api:recipes-download-shopping-cart')
    #     )
    # shopping_cart.short_description = "Download file"


class SubscriberAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "author"
    )


class TokenAdmin(admin.ModelAdmin):
    list_display = ("key", "user")


admin.site.register(User, UserAdmin)
admin.site.register(Subscriber, SubscriberAdmin)
admin.site.register(ProxyToken, TokenAdmin)
admin.site.unregister(Group)
admin.site.unregister(BaseToken)
