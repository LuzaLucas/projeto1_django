from django import forms
from recipes.models import Recipe
from utils.django_forms import add_attr
from utils.strings import is_positive_number
from collections import defaultdict
from django.core.exceptions import ValidationError


class AuthorRecipeForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self._myerrors = defaultdict(list)
        
        add_attr(self.fields.get('preparation_steps'), 'class', 'span-2')
    
    class Meta:
        model = Recipe
        fields = 'title', 'description', 'preparation_time', \
            'preparation_time_unit', 'servings', 'servings_unit', \
            'preparation_steps', 'cover'
        widgets = {
            'cover': forms.FileInput(
                attrs={
                    'class': 'span-2'
                }
            ),
            'servings_unit': forms.Select(
                choices=(
                    ('Porções', 'Porções'),
                    ('Pedaços', 'Pedaços'),
                    ('Servidas', 'Servidas'),
                    ('Pessoas', 'Pessoas'),
                ),
            ),
            'preparation_time_unit': forms.Select(
                choices=(
                    ('Minutos', 'Minutos'),
                    ('Horas', 'Horas'),
                ),
            ),
        }
        
    
    def clean(self, *args, **kwargs):
        super_clean = super().clean(*args, **kwargs)
        cleaneddata = self.cleaned_data
        
        title = cleaneddata.get('title')
        description = cleaneddata.get('description')
        
        if len(title) < 5: # type: ignore
            self._myerrors['title'].append('Title must have at least 5 characters')
            
        if title == description:
            self._myerrors['title'].append('Cannot be equal to description')
            self._myerrors['description'].append('Cannot be equal to title')
        
        if self._myerrors:
            raise ValidationError(self._myerrors)
        
        return super_clean
    
    
    def clean_preparation_time(self):
        field_name = 'preparation_time'
        field_value = self.cleaned_data.get(field_name)
        
        if not is_positive_number(field_value):
            self._myerrors[field_name].append('Must be a positive number')
            
        return field_value
    
    
    def clean_servings(self):
        field_name = 'servings'
        field_value = self.cleaned_data.get(field_name)
        
        if not is_positive_number(field_value):
            self._myerrors[field_name].append('Must be a positive number')
            
        return field_value
