from django.urls import path
from .views import site
from .views import api


app_name = 'recipes'

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
         'recipes/api/v2/', 
         api.RecipeAPIv2ViewSet.as_view({
               'get': 'list',
               'post': 'create',    
          }), 
         name="recipe_api_v2"
     ),
    path(
         'recipes/api/v2/<int:pk>/', 
         api.RecipeAPIv2ViewSet.as_view({
               'get': 'retrieve',
               'patch': 'partial_update',
               'delete': 'destroy',
          }), 
         name="recipe_api_v2_detail"
     ),
    path(
         'recipes/api/v2/tag/<int:pk>/', 
         api.tag_api_detail, 
         name="recipe_api_v2_tag"
     ),
]
