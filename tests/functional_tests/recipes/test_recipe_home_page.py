from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import pytest
from .base import RecipeBaseFunctionalTest
from unittest.mock import patch


@pytest.mark.functional_test
class RecipeHomePageFunctionalTest(RecipeBaseFunctionalTest):
    @patch('recipes.views.PER_PAGE', new=3)
    def test_recipe_home_page_without_recipes_not_found_message(self):
        # self.make_recipe_in_batch(qtd=20)
        self.browser.get(self.live_server_url)
        body = self.browser.find_element(By.TAG_NAME, 'body')
        # self.sleep()
        self.assertIn('No recipes found here', body.text)
        
        
    @patch('recipes.views.PER_PAGE', new=3)
    def test_recipe_search_input_can_find_correct_recipes(self):
        recipes = self.make_recipe_in_batch()
        
        # user opens the page
        self.browser.get(self.live_server_url)
        
        title_needed = 'This is what I want'
        
        recipes[0].title = title_needed
        recipes[0].save()
        
        # Sees the search field with the text "Search for a recipe here"
        search_input = self.browser.find_element(
            By.XPATH,
            '//input[@placeholder="Search for a recipe here"]'
        )
        
        # Clicks on input and type the search term "Recipe title 1"
        # to find the recipe with this title
        search_input.send_keys(title_needed)
        self.sleep(2)
        
        search_input.send_keys(Keys.ENTER)
        
        # The user finds out what he was looking for
        self.assertIn(
            title_needed,
            self.browser.find_element(By.CLASS_NAME, 'main-content-list').text
        )
        
        self.sleep(3)
