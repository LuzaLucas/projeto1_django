from django.test import TestCase
from django.urls import reverse, resolve
from recipes import views
from recipes.models import Category, Recipe, User


class RecipeViewsTest(TestCase):
    # home
    def test_recipe_home_view_function_is_correct(self):
        # view = resolve('/') 
        view = resolve(reverse('recipes:home')) # same thing
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
        
    def test_recipe_home_template_loads_recipes(self):
        # category = Category(name='categoria_aleatória') # same shit
        # category.save()
        category = Category.objects.create(name='categoria_aleatória')
        author = User.objects.create(
            first_name='user',
            last_name='name',
            username='username',
            password='123456',
            email='username@email.com',
        )
        recipe = Recipe.objects.create(
            category=category,
            author=author,
            title = 'Recipe Title',
            description = 'Recipe Description',
            slug = 'recipe-slug',
            preparation_time = 10,
            preparation_time_unit = 'minutes',
            servings = 5,
            servings_unit = 'porções',
            preparation_steps = 'recipe preparation steps',
            preparation_steps_is_html = False,
            is_published = True,
        )
        
        response = self.client.get(reverse('recipes:home'))
        content = response.content.decode('utf-8')
        response_context_recipes = response.context['recipes']
        self.assertIn('Recipe Title', content)
        self.assertIn('5 porções', content)
        self.assertEqual(len(response_context_recipes), 1)
        
        ...
        
    # category
    def test_recipe_category_view_function_is_correct(self):
        view = resolve(reverse('recipes:category', kwargs={'category_id': 1000}))
        self.assertIs(view.func, views.category)
        
    def test_recipe_category_view_return_status_code_404_if_no_recipes_found(self):
        response = self.client.get(
            reverse('recipes:category', kwargs={'category_id': 1000}))
        self.assertEqual(response.status_code, 404)
        
    # recipe / detail
    def test_recipe_detail_view_function_is_correct(self):
        view = resolve(reverse('recipes:recipe', kwargs={'id': 1}))
        self.assertIs(view.func, views.recipe)
        
    def test_recipe_detail_view_return_status_code_404_if_no_recipes_found(self):
        response = self.client.get(
            reverse('recipes:recipe', kwargs={'id': 1000}))
        self.assertEqual(response.status_code, 404)
