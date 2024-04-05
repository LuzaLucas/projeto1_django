from unittest import TestCase
from django.test import TestCase as DjangoTestCase
from authors.forms import RegisterForm
from parameterized import parameterized
from django.urls import reverse


class AuthorRegisterFormUnitTest(TestCase):
    @parameterized.expand([
        ('username', 'Your username goes here'),
        ('first_name', 'Your first name goes here'),
        ('last_name', 'Your last name goes here'),
        ('email', 'Your email goes here'),
        ('password', 'Your password'),
        ('password2', 'Repeat your password here'),
    ])
    def test_fields_placeholder(self, field, placeholder):
        form = RegisterForm()
        field_widget = form[field].field.widget
        current_placeholder = field_widget.attrs.get('placeholder')
        self.assertEqual(current_placeholder, placeholder) 
        

    @parameterized.expand([
        ('email', 'The email must be valid'),
        ('password', 'Password must have at least one uppercase letter, one lowercase '
            'letter and one number. The length should be at least 8 characters.'),
        ('username', 'Username must have letters, number or some of those @/./+/=/_. '
            'The length should be between 4 and 150 characters.'),
    ])
    def test_fields_help_text(self, field, needed):
        form = RegisterForm()
        current = form[field].field.help_text
        self.assertEqual(current, needed)
        

    @parameterized.expand([
        ('first_name', 'First name'),
        ('last_name', 'Last name'),
        ('username', 'Username'),
        ('email', 'E-mail'),
        ('password', 'Password'),
        ('password2', 'Password2'),
    ])
    def test_fields_label(self, field, needed):
        form = RegisterForm()
        current = form[field].field.label
        self.assertEqual(current, needed)
        
        
class AuthorRegisterFormIntegrationTest(DjangoTestCase):
    def setUp(self, *args, **kwargs) -> None:
        self.form_data = {
            'username': 'user',
            'first_name': 'first',
            'last_name': 'last',
            'email': 'email@email.com',
            'password': 'Str0ngP@ssword1',
            'password2': 'Str0ngP@ssword1',
        }
        return super().setUp(*args, **kwargs)
    
    @parameterized.expand([
        ('username', 'This field must not be empty'),
        ('first_name', 'Write your first name'),
        ('last_name', 'Write your last name'),
        ('email', 'Email is required'),
        ('password', 'Password must not be empty'),
        ('password2', 'Please, repeat your password'),
    ])
    def test_fields_cannot_be_empty(self, field, msg):
        self.form_data[field] = ''
        url = reverse('authors:register_create')
        response = self.client.post(url, data=self.form_data, follow=True)
        
        self.assertIn(msg, response.content.decode('utf-8'))
        self.assertIn(msg, response.context['form'].errors.get(field))
        
        
    def test_username_field_min_length_should_be_150(self):
        self.form_data['username'] = 'a' * 151
        url = reverse('authors:register_create')
        response = self.client.post(url, data=self.form_data, follow=True)
        
        # msg = 'Username must have at leaset 4 characters'
        msg = 'Username must have less than 151 characters'
        self.assertIn(msg, response.content.decode('utf-8'))
        self.assertIn(msg, response.context['form'].errors.get('username'))
        
        
    def test_password_field_have_lower_upper_case_letters_and_numbers(self):
        self.form_data['password'] = 'abc123'
        url = reverse('authors:register_create')
        response = self.client.post(url, data=self.form_data, follow=True)
        
        msg = ('Password must have at least one uppercase letter, one lowercase '
            'letter and one number. The length should be at least 8 characters.')
        
        self.assertIn(msg, response.context['form'].errors.get('password'))
        self.assertIn(msg, response.content.decode('utf-8'))
        
        
    def test_password_and_password_confirmation_are_equal(self):
        self.form_data['password'] = '@A123abc123'
        self.form_data['password2'] = '@A123abc1235'

        url = reverse('authors:register_create')
        response = self.client.post(url, data=self.form_data, follow=True)

        msg = 'Password and password 2 must match'

        self.assertIn(msg, response.context['form'].errors.get('password'))
        self.assertIn(msg, response.content.decode('utf-8'))

        self.form_data['password'] = '@A123abc123'
        self.form_data['password2'] = '@A123abc123'

        url = reverse('authors:register_create')
        response = self.client.post(url, data=self.form_data, follow=True)

        self.assertNotIn(msg, response.content.decode('utf-8'))
        
        
    def test_send_get_request_to_registration_create_view_returns_404(self):
        url = reverse('authors:register_create')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)
        
        
    def test_email_field_must_be_unique(self):
        url = reverse('authors:register_create')
        
        self.client.post(url, data=self.form_data, follow=True)
        
        response = self.client.post(url, data=self.form_data, follow=True)
        
        msg = 'User email is already in use'
        
        self.assertIn(msg, response.context['form'].errors.get('email'))
        self.assertIn(msg, response.content.decode('utf-8'))


    def test_author_created_can_login(self):
        url = reverse('authors:register_create')
        
        self.form_data.update({
            'username': 'testuser',
            'password': 'Abc12345@',
            'password2': 'Abc12345@',
        })
        
        self.client.post(url, data=self.form_data, follow=True)
        
        is_authenticated = self.client.login(
            username='testuser',
            password='Abc12345@',
        )
        
        self.assertTrue(is_authenticated)
