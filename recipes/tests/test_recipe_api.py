from rest_framework import test
from django.urls import reverse
from recipes.tests.test_recipe_base import RecipeMixin
from unittest.mock import patch


class RecipeAPIv2Test(test.APITestCase, RecipeMixin):
    def get_recipe_api_list(self):
        api_url = reverse('recipes:recipes-api-list')
        response = self.client.get(api_url)
        return response
    
    def test_recipe_api_list_returns_status_code_200(self):
        response = self.get_recipe_api_list()
        self.assertEqual(response.status_code, 200)

    @patch('recipes.views.api.RecipeAPIv2Pagination.page_size', new=8)
    def test_recipe_api_list_loads_correct_number_of_recipes(self):
        wanted_number_of_recipes = 8
        self.make_recipe_in_batch(qtd=wanted_number_of_recipes)
        
        response = self.client.get(reverse(
            'recipes:recipes-api-list') + '?page=1')
        qtt_of_loaded_recipes = len(response.data.get('results')) # type: ignore
        
        self.assertEqual(wanted_number_of_recipes, qtt_of_loaded_recipes)

    def test_recipe_api_list_do_not_show_not_published_recipes(self):
        recipes = self.make_recipe_in_batch(qtd=2)
        recipe_not_published = recipes[0]
        recipe_not_published.is_published = False
        recipe_not_published.save()
        response = self.get_recipe_api_list()
        self.assertEqual(
            len(response.data.get('results')), 1 # type: ignore
        )
        
        