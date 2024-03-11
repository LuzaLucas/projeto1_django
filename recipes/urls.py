from django.urls import path
from recipes import views


urlpatterns = [
    path('', views.home), # Home
    path('recipes/<int:id>/', views.recipe),
]
