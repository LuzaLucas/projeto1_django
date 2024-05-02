from utils.strings import is_positive_number
from collections import defaultdict
from django.core.exceptions import ValidationError


class AuthorRecipeValidator():
    def __init__(self, data, errors=None, ErrorClass=None) -> None:
        self.errors = defaultdict(list) if errors is None else errors
        self.ErrorClass = ValidationError if ErrorClass is None else ErrorClass
        self.data = data
        self.clean()
        
    
    def clean(self, *args, **kwargs):
        self.clean_title()
        self.clean_servings()
        self.clean_preparation_time()
        
        cleaneddata = self.data
        
        title = cleaneddata.get('title')
        description = cleaneddata.get('description')
            
        if title == description:
            self.errors['title'].append('Cannot be equal to description')
            self.errors['description'].append('Cannot be equal to title')
        
        if self.errors:
            raise self.ErrorClass(self.errors)
    
    
    def clean_title(self):
        title = self.data.get('title')
        
        if len(title) < 5: # type: ignore
            self.errors['title'].append('Title must have at least 5 characters')
            
        return title
    
    
    def clean_preparation_time(self):
        field_name = 'preparation_time'
        field_value = self.data.get(field_name)
        
        if not is_positive_number(field_value):
            self.errors[field_name].append('Must be a positive number')
            
        return field_value
    
    
    def clean_servings(self):
        field_name = 'servings'
        field_value = self.data.get(field_name)
        
        if not is_positive_number(field_value):
            self.errors[field_name].append('Must be a positive number')
            
        return field_value
