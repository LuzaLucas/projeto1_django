from django.urls import reverse, resolve
from recipes import views
from .test_recipe_base import RecipeTestBase
from unittest import skip


class RecipeViewsTest(RecipeTestBase):
    # home
    def test_recipe_home_view_function_is_correct(self):
        # view = resolve('/') # same shit
        view = resolve(reverse('recipes:home'))
        self.assertIs(view.func, views.home)
        
        
    def test_recipe_home_view_return_status_code_200_OK(self):
        response = self.client.get(reverse('recipes:home'))
        self.assertEqual(response.status_code, 200)
        
        
    def test_recipe_home_view_loads_correct_template(self):
        response = self.client.get(reverse('recipes:home'))
        self.assertTemplateUsed(response, 'recipes/pages/home.html')
        
        
    def test_recipe_home_template_shows_no_recipes_found_if_no_recipes(self):
        response = self.client.get(reverse('recipes:home'))
        self.assertIn('<h1>No recipes found here.</h1>', 
            response.content.decode('utf-8'))
        
    
    @skip('Why am i skiping this test / WIP (work in progress)')
    def test_recipe_home_template_loads_recipes(self):
        #need a recipe for this test
        self.make_recipe(category_data={
            'name': 'breakfast'
        })
        
        response = self.client.get(reverse('recipes:home'))
        content = response.content.decode('utf-8')
        response_context_recipes = response.context['recipes']
        
        # checks if one recipe exists
        self.assertIn('breakfast', content)
        self.assertEqual(len(response_context_recipes), 1)
        
        # got to write more stuff here
        self.fail('Finish testing stuff')
        
        
    def test_recipe_home_template_dont_load_recipes_not_published(self):
        """Test if recipe is_published False = don't show"""
        # need a recipe for this test
        self.make_recipe(is_published=False)
        
        response = self.client.get(reverse('recipes:home'))
        
        # checks if one recipe exists
        self.assertIn('<h1>No recipes found here.</h1>', 
            response.content.decode('utf-8'))
        
        
    # category
    def test_recipe_category_template_loads_recipes(self):
        needed_title = 'This is a category test.'
        # need a recipe for this test
        self.make_recipe(title=needed_title)
        
        response = self.client.get(reverse('recipes:category', args=(1,)))
        content = response.content.decode('utf-8')
        
        # checking if one recipe exists
        self.assertIn(needed_title, content)
        
        
    def test_recipe_category_template_dont_load_recipes_not_published(self):
        """Test if recipe is_published False = don't show"""
        recipe = self.make_recipe(is_published=False)
        
        # need a recipe for this test
        response = self.client.get(
            reverse('recipes:recipe', kwargs={'id': recipe.category.id})) # type: ignore
        
        self.assertEqual(response.status_code, 404)
        
        
    def test_recipe_category_view_function_is_correct(self):
        view = resolve(reverse('recipes:category', kwargs={'category_id': 1000}))
        self.assertIs(view.func, views.category)
        
        
    def test_recipe_category_view_return_status_code_404_if_no_recipes_found(self):
        response = self.client.get(
            reverse('recipes:category', kwargs={'category_id': 1000}))
        self.assertEqual(response.status_code, 404)
        
        
    # recipe / detail
    def test_recipe_detail_template_loads_the_correct_recipe(self):
        needed_title = 'This is a detail page - It loads one recipe.'
        
        # need a recipe for this test
        self.make_recipe(title=needed_title)
        
        response = self.client.get(reverse('recipes:recipe', 
            kwargs={'id': 1}))
        content = response.content.decode('utf-8')
        
        # checking if one recipe exists
        self.assertIn(needed_title, content)
        
        
    def test_recipe_detail_view_function_is_correct(self):
        view = resolve(reverse('recipes:recipe', kwargs={'id': 1}))
        self.assertIs(view.func, views.recipe)
        
        
    def test_recipe_detail_view_return_status_code_404_if_no_recipes_found(self):
        response = self.client.get(
            reverse('recipes:recipe', kwargs={'id': 1000}))
        self.assertEqual(response.status_code, 404)
