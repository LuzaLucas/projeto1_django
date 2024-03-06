from django.shortcuts import render
from django.http import HttpResponse


def home(request):
    return render(
        request,
        'recipes/home.html',
        {'name': 'Lucas',}
    )


def sobre(request):
    return HttpResponse('SOBRE 1')


def contato(request):
    return HttpResponse('CONTATO 1')


