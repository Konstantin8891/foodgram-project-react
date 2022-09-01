from django.core.paginator import Paginator
from django.conf import settings


def paginator_method(request, recipes):
    paginator = Paginator(recipes, settings.RECIPE_AMOUNT)
    page_number = request.GET.get('page')
    return paginator.get_page(page_number)