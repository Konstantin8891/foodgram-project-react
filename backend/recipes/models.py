from django.db import models

from users.models import User


class Tag(models.Model):
    slug = models.SlugField(unique=True)
    name = models.CharField(max_length=50, unique=True)
    color = models.CharField(max_length=7)

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    name = models.CharField(max_length=100)
    measurement_unit = models.CharField(max_length=100)


class Recipe(models.Model):
    author = models.ForeignKey(User ,on_delete=models.CASCADE, related_name='recipes')
    name = models.CharField('Название рецепта', max_length=200, help_text='Введите название рецепта', unique=True)
    image = models.ImageField(upload_to='posts/')
    text = models.TextField('Текст рецепта', help_text='Введите текст рецепта')
    ingredients = models.ManyToManyField(Ingredient, through='RecipeIngredient', related_name='recipes')
    tags = models.ManyToManyField(Tag, related_name='recipes')
    cooking_time = models.IntegerField('Время приготовления в минутах', help_text='Введите время пригтовления в минутах')
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    amount = models.IntegerField()


class ShoppingCart(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='shopping_cart'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='shopping_cart'
    )


class Favorite(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='favorite'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='favorite'
    )


class Subscriber(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='follower'
    )
    # id
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='following'
    )