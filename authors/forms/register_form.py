from typing import Any
from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from utils.django_forms import add_attr, strong_password


class RegisterForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        add_attr(self.fields['username'],'placeholder', 'Your username goes here')
        add_attr(self.fields['email'],'placeholder', 'Your email goes here')
        add_attr(self.fields['first_name'],'placeholder', 'Your first name goes here')
        add_attr(self.fields['last_name'],'placeholder', 'Your last name goes here')
        add_attr(self.fields['username'], 'css', 'a-css-class')
    
    username = forms.CharField(
        label='Username',
        help_text=(
            'Username must have letters, number or some of those @/./+/=/_. '
            'The length should be between 4 and 150 characters.'
        ),
        error_messages={
            'required': 'This field must not be empty',
            'min_length': 'Username must have at leaset 4 characters',
            'max_length': 'Username must have less than 151 characters',
        },
        min_length=4, max_length=150,
    )
    first_name = forms.CharField(
        error_messages={'required': 'Write your first name'},
        label='First name',
    )
    last_name = forms.CharField(
        error_messages={'required': 'Write your last name'},
        label='Last name',
    )
    email = forms.EmailField(
        error_messages={'required': 'Email is required'},
        label='E-mail',
        help_text='The email must be valid',
        
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Your password'
        }),
        error_messages={
            'required': 'Password must not be empty'
        },
        help_text=(
            'Password must have at least one uppercase letter, one lowercase '
            'letter and one number. The length should be at least 8 characters.'
        ),
        validators=[strong_password],
        label='Password'
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Repeat your password here'
        }),
        error_messages={
            'required': 'Please, repeat your password'
        },
        label='Password2'
    )
    
    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'username',
            'email',
            'password',
        ]
        widgets = {
            'first_name': forms.TextInput(attrs={
                'placeholder': 'Type your first name here',
                'class': 'input text-input',
            }),
            'password': forms.PasswordInput(attrs={
                'placeholder': 'Type your password here',
            })
        }
    
    
    def clean_email(self):
        email = self.cleaned_data.get('email', '')
        exists = User.objects.filter(email=email).exists()
        
        if exists:
            raise ValidationError('User email is already in use', code='invalid',)
        
        return email
    
    
    def clean(self) -> dict[str, Any]: #type: ignore
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password2 = cleaned_data.get('password2')
        
        if password != password2:
            raise ValidationError({
                'password': 'Password and password 2 must match',
                'password2': 'Password and password 2 must match'
            })
