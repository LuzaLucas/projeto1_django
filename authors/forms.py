from typing import Any
from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
import re


def add_attr(field, attr_name, attr_new_val):
    existing_attr = field.widget.attrs.get(attr_name, '')
    field.widget.attrs[attr_name] = f'{existing_attr} {attr_new_val}'.strip()
    
    
def add_placeholder(field, placeholder_val):
    add_attr(field, 'placeholder', placeholder_val)
    
    
def strong_password(password):
    regex = re.compile(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9]).{8,}$')
    
    if not regex.match(password):
        raise ValidationError((
            'Password must have at least one uppercase letter, one lowercase '
            'letter and one number. The length should be at least 8 characters.'
        ),
        code='Invalid'
        )


class RegisterForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        add_attr(self.fields['username'],'placeholder', 'Your Username goes here :)')
        add_attr(self.fields['email'],'placeholder', 'Your Email goes here :)')
        add_attr(self.fields['last_name'],'placeholder', 'Your Last name goes here :)')
        add_attr(self.fields['username'], 'css', 'a-css-class')
    
    password = forms.CharField(
        required=True,
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
        validators=[strong_password]
    )
    password2 = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Repeat your password here'
        })
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
        # exclude = ['first_name']
        labels = {
            'username': 'Username',
            'first_name': 'First name',
            'last_name': 'Last name',
            'email': 'E-mail',
            'password': 'Password'
        }
        help_texts = {
            'email': 'The email must be valid'
        }
        error_messages = {
            'username': {
                'required': 'This field must not be empty',
            }
        }
        widgets = {
            'first_name': forms.TextInput(attrs={
                'placeholder': 'Type your first name here',
                'class': 'input text-input',
            }),
            'password': forms.PasswordInput(attrs={
                'placeholder': 'Type your password here',
            })
        }
        
        
    def clean_password(self):
        data = self.cleaned_data.get('password')
        
        if 'atenção' in data: #type: ignore
            raise ValidationError(
                'Não digite %(value)s no campo password',
                code='invalid',
                params={ 'value': '"atenção"' }
            )
        
        return data
    
    
    def clean_first_name(self): 
        data = self.cleaned_data.get('first_name')
        
        if 'John Doe' in data: #type: ignore
            raise ValidationError(
                'Não digite %(value)s no campo first name',
                code='invalid',
                params={ 'value': '"John Doe"' }
            )
        
        return data
    
    
    def clean(self) -> dict[str, Any]: #type: ignore
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password2 = cleaned_data.get('password2')
        
        if password != password2:
            raise ValidationError({
                'password': 'Password and password 2 must match',
                'password2': 'Password and password 2 must match'
            })
