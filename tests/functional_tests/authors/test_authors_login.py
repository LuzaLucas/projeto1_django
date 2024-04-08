from .base import AuthorsBaseTest
import pytest
from django.contrib.auth.models import User
from django.urls import reverse
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys


@pytest.mark.functional_test
class AuthorsLoginText(AuthorsBaseTest):
    def test_user_valid_data_can_login_successfully(self):
        string_password = 'pass'
        user = User.objects.create_user(
            username='my_user', password=string_password)
        
        # User open login page
        self.browser.get(self.live_server_url + reverse('authors:login'))
        
        # User sees a login form
        form = self.browser.find_element(By.CLASS_NAME, 'main-form')
        username_field = self.get_by_placeholder(form, 'Type your username')
        password_field = self.get_by_placeholder(form, 'Type your password')
        
        # User types his username and password
        username_field.send_keys(user.username)
        password_field.send_keys(string_password)
        
        # User send a form
        form.submit()
        
        # User sees the successfull login message and his username
        self.assertIn(
            f'You are logged in as {user.username}.',
            self.browser.find_element(By.TAG_NAME, 'body').text
        )
        
        
    def test_login_create_raises_404_if_not_POST_method(self):
        self.browser.get(self.live_server_url + reverse('authors:login_create'))
        
        self.assertIn(
            'Not Found',
            self.browser.find_element(By.TAG_NAME, 'body').text
        )
        
        
    def test_form_login_is_invalid(self):
        # User open login page
        self.browser.get(
            self.live_server_url + reverse('authors:login')
        )
        
        # User sees the login form
        form = self.browser.find_element(By.CLASS_NAME, 'main-form')
        
        # User try to send empty values
        username = self.get_by_placeholder(form, 'Type your username')
        password = self.get_by_placeholder(form, 'Type your password')
        username.send_keys(' ')
        password.send_keys(' ')
        
        # User sends the form
        form.submit()
        
        # Sees the error message
        self.assertIn(
            'Invalid username or password',
            self.browser.find_element(By.TAG_NAME, 'body').text
        )
        
        
    def test_form_login_invalid_credentials(self):
        # User open login page
        self.browser.get(
            self.live_server_url + reverse('authors:login')
        )
        
        # User sees the login form
        form = self.browser.find_element(By.CLASS_NAME, 'main-form')
        
        # User try to send invalid user and/or password
        username = self.get_by_placeholder(form, 'Type your username')
        password = self.get_by_placeholder(form, 'Type your password')
        username.send_keys('invalid_user')
        password.send_keys('invalid_password')
        
        # User sends the form
        form.submit()
        
        # Sees the error message
        self.assertIn(
            'Invalid credentials',
            self.browser.find_element(By.TAG_NAME, 'body').text
        )
    