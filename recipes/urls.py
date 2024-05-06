from django.urls import path
from .views import site
from .views import api
from rest_framework.routers import SimpleRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)


app_name = 'recipes'

recipe_api_v2_router = SimpleRouter()
recipe_api_v2_router.register('recipes/api/v2', api.RecipeAPIv2ViewSet, 
    basename='recipes-api',)

urlpatterns = recipe_api_v2_router

urlpatterns = [
    path(
         '', 
         site.RecipeListViewHome.as_view(), 
         name="home"),
    path(
         'recipes/search/',
         site.RecipeListViewSearch.as_view(), 
         name="search"
     ),
    path(
         'recipes/tags/<slug:slug>',
         site.RecipeListViewTag.as_view(), 
         name="tag"
     ),
    path(
         'recipes/category/<int:category_id>/',
         site.RecipeListViewCategory.as_view(), 
         name="category"
     ),
    path(
         'recipes/<int:pk>/', 
         site.RecipeDetail.as_view(), 
         name="recipe"
     ),
    path(
         'recipes/api/v1/', 
         site.RecipeListViewHomeApi.as_view(), 
         name="recipe_api_v1"
     ),
    path(
         'recipes/api/v1/<int:pk>/', 
         site.RecipeDetailApi.as_view(), 
         name="recipe_api_v1_detail"
     ),
    path(
         'recipes/theory/', 
         site.theory, 
         name="theory"
     ),
    path(
         'recipes/api/v2/tag/<int:pk>/', 
         api.tag_api_detail, 
         name="recipe_api_v2_tag"
     ),
    
    # JWT urls
    path(
         'recipes/api/token/', 
         TokenObtainPairView.as_view(), 
         name='token_obtain_pair'
     ),
    path(
         'recipes/api/token/refresh/', 
         TokenRefreshView.as_view(), 
         name='token_refresh'
     ),
    path(
         'recipes/api/token/verify/',
         TokenVerifyView.as_view(), 
         name='token_verify'
     ),
]

urlpatterns += recipe_api_v2_router.urls
