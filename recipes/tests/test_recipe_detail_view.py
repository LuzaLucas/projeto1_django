from django.urls import reverse, resolve
from recipes.views import site
from .test_recipe_base import RecipeTestBase
from unittest import skip


class RecipeDetailViewTest(RecipeTestBase):
    def test_recipe_detail_template_loads_the_correct_recipe(self):
        needed_title = 'This is a detail page - It loads one recipe.'
        
        # need a recipe for this test
        self.make_recipe(title=needed_title)
        
        response = self.client.get(reverse('recipes:recipe', 
            kwargs={'pk': 1}))
        content = response.content.decode('utf-8')
        
        # checking if one recipe exists
        self.assertIn(needed_title, content)
        
        
    def test_recipe_detail_view_function_is_correct(self):
        view = resolve(reverse('recipes:recipe', kwargs={'pk': 1}))
        self.assertIs(view.func.view_class, site.RecipeDetail)
        
        
    def test_recipe_detail_view_return_status_code_404_if_no_recipes_found(self):
        response = self.client.get(
            reverse('recipes:recipe', kwargs={'pk': 1000}))
        self.assertEqual(response.status_code, 404)
