from rest_framework import test
from django.urls import reverse
from recipes.tests.test_recipe_base import RecipeMixin
from unittest.mock import patch


class RecipeAPIv2TestMixin(test.APITestCase, RecipeMixin):
    def get_recipe_list_reverse_url(self, reverse_result=None):
        api_url = reverse_result or reverse('recipes:recipes-api-list')
        return api_url
    
    def get_recipe_api_list(self, reverse_result=None):
        api_url = self.get_recipe_list_reverse_url(reverse_result)
        response = self.client.get(api_url)
        return response
    
    def get_auth_data(self, username='user', password='pass'):
        userdata = {
            'username': username,
            'password': password,
        }
        user = self.make_author(
            username=userdata.get('username'), # type: ignore
            password=userdata.get('password') # type: ignore
        )
        response = self.client.post(
            reverse('recipes:token_obtain_pair'), data={**userdata}
        )
        return {
            'jwt_access_token': response.data.get('access'), # type: ignore
            'jwt_refresh_token': response.data.get('refresh'), # type: ignore
            'user': user, # type: ignore
        }
    
    def get_recipe_raw_data(self):
        return {
            'title': 'This is the title',
            'description': 'This is the description',
            'preparation_time': 1,
            'preparation_time_unit': 'Minutos',
            'servings': 1,
            'servings_unit': 'Pessoas',
            'preparation_steps': 'This are the preparation steps.'
        }


class RecipeAPIv2Test(RecipeAPIv2TestMixin):
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
    
    @patch('recipes.views.api.RecipeAPIv2Pagination.page_size', new=10)
    def test_recipe_api_list_loads_recipes_by_category_id(self):
        # creating categories
        category_wanted = self.make_category(name='WANTED_CATEGORY')
        category_not_wanted = self.make_category(name='NOT_WANTED_CATEGORY')
        
        # creating 10 recipes
        recipes = self.make_recipe_in_batch(qtd=10)
        
        # changing all recipes to the wanted category
        for recipe in recipes:
            recipe.category = category_wanted
            recipe.save()
        
        # changing 1 recipe to the unwanted category
        # as a result, this recipe should NOT show in the page
        recipes[0].category = category_not_wanted
        recipes[0].save()
        
        # action: get recipes by wanted_category_id
        api_url = reverse('recipes:recipes-api-list') + f'?category_id={category_wanted.id}' # type: ignore
        response = self.get_recipe_api_list(reverse_result=api_url)
        
        # we should only see recipes from the wanted category
        self.assertEqual(
            len(response.data.get('results')), 9 # type: ignore
        )
        
    def test_recipe_api_list_user_must_send_jwt_token_to_create_recipe(self):
        api_url = self.get_recipe_list_reverse_url()
        response = self.client.post(api_url)
        self.assertEqual(
            response.status_code, 401
        )
        
    def test_recipe_api_list_logged_user_can_create_a_recipe(self):
        recipe_raw_data = self.get_recipe_raw_data()
        auth_data = self.get_auth_data()
        jwt_access_token = auth_data.get('jwt_access_token')
        
        # data['preparation_time'] = -1
        
        response = self.client.post(
            self.get_recipe_list_reverse_url(),
            data=recipe_raw_data,
            # content_type='application/json',
            HTTP_AUTHORIZATION=f'Bearer {jwt_access_token}'
        )
        self.assertEqual(
            response.status_code, 201
        )
        
        
        # self.assertEqual(
        #     response.status_code, 400
        # )
        # self.assertEqual(
        #     response.data.get('preparation_time')[0],
        #     'Must be a positive number'
        # )
        
        # print(response.data.get('title')[0]) # type: ignore
        # self.assertEqual(
        #     response.data.get('title')[0], # type: ignore
        #     'This field is required.'
        # )
        
    def test_recipe_api_list_logged_user_can_update_a_recipe(self):
        # Arrange (config)
        recipe = self.make_recipe()
        access_data = self.get_auth_data(username='test_patch')
        jwt_access_token = access_data.get('jwt_access_token')
        author = access_data.get('user')
        recipe.author = author
        recipe.save()
        
        wanted_new_title = f'The new title updated by {author.username}' # type: ignore

        # Action
        response = self.client.patch(
            reverse('recipes:recipes-api-detail', args=(recipe.id,)), # type: ignore
            data={'title': wanted_new_title},
            HTTP_AUTHORIZATION=f'Bearer {jwt_access_token}'
        )
        
        # Assertion
        self.assertEqual(
            response.data.get('title'), wanted_new_title # type: ignore
        )
        self.assertEqual(
            response.status_code, 200
        )
        
    def test_recipe_api_list_logged_user_cant_update_a_recipe_owned_by_another_user(self):
        # Arrange (config)
        recipe = self.make_recipe()
        access_data = self.get_auth_data(username='test_patch')
        
        # This user cannot update the recipe
        another_user = self.get_auth_data(username='second_user')
        jwt_access_token_from_another_user = another_user.get('jwt_access_token')
        
        # This is the actual owner of the recipe
        author = access_data.get('user')
        recipe.author = author
        recipe.save()
        
        # Action
        response = self.client.patch(
            reverse('recipes:recipes-api-detail', args=(recipe.id,)), # type: ignore
            data={},
            HTTP_AUTHORIZATION=f'Bearer {jwt_access_token_from_another_user}'
        )
        
        # Assertion
        self.assertEqual(
            response.status_code, 403
        )
        