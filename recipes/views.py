from django.shortcuts import render
from django.http import Http404
from utils.recipes.factory import make_recipe
from .models import Recipe


def home(request):
    recipes = Recipe.objects.filter(is_published=True).order_by('-id')
    return render(
        request,
        'recipes/pages/home.html',
        {'recipes': recipes,}
    )


def category(request, category_id):
    recipes = Recipe.objects.filter(
        category__id=category_id, is_published=True).order_by('-id')
    
    if not recipes:
        raise Http404('Página não encontrada')

    return render(
        request,
        'recipes/pages/category.html',
        {'recipes': recipes,
         'title': f'{recipes.first().category.name} - Category |'} #type: ignore
    )


def recipe(request, id):
    return render(
        request,
        'recipes/pages/recipe-view.html',
        {'recipe': make_recipe(), 'is_detail_page': True,}
    )

