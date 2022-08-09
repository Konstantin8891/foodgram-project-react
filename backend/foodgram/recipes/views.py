from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from .models import Recipe
from .paginator import paginator_method
from .forms import RecipeForm

def index(request):
    recipes = Recipe.objects.select_related('author').prefetch_related('ingridient', 'tag').all()
    template = 'recipes/index.html'
    page_obj = paginator_method(request, recipes)
    context = {'page_obj': page_obj}
    return render(request, template, context)

@login_required
def recipe_create(request):
    template = 'recipes/recipe_create.html'
    form = RecipeForm(request.POST or None, files=request.FILES or None)
    if form.is_valid():
        post = form.save(commit=False)
        post.author = request.user
        post.save()
        return redirect('recipes:index', post.author)
    context = {'form': form, }
    return redirect(request, template, context)
