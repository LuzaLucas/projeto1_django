from .base import AuthorsBaseTest
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys


class AuthorRegisterTest(AuthorsBaseTest):
    def get_by_placeholder(self, web_element, placeholder):
        return web_element.find_element(
            By.XPATH, f'//input[@placeholder="{placeholder}"]')
        
    def fill_form_dummy_data(self, form):
        fields = form.find_elements(By.TAG_NAME, 'input')
        for field in fields:
            if field.is_displayed():
                field.send_keys(' ' * 20)
    
    
    def test_empty_last_name_error_message(self):
        self.browser.get(self.live_server_url + '/authors/register/')
        form = self.browser.find_element(
            By.XPATH,
            '/html/body/main/div[2]/form'
        )
        
        self.fill_form_dummy_data(form)
        form.find_element(By.NAME, 'email').send_keys('dummy@email.com')
        
        first_name_field = self.get_by_placeholder(form, 'Your first name goes here')
        first_name_field.send_keys('Atention please')
        first_name_field.send_keys(Keys.ENTER)
        
        form = self.browser.find_element(
            By.XPATH,
            '/html/body/main/div[2]/form'
        )
        self.sleep(2)
        self.assertIn('Write your last name', form.text)
        
        self.sleep(2)
        