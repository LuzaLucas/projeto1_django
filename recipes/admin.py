from django.contrib import admin
from .models import Category, Recipe
from django.contrib.contenttypes.admin import GenericStackedInline
from tag.models import Tag


class CategoryAdmin(admin.ModelAdmin):
    ...
    
    
class TagInLine(GenericStackedInline):
    model = Tag
    fields = 'name',
    extra = 1


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = 'id', 'title', 'created_at', 'is_published',
    list_display_links = 'id', 'title',
    search_fields = 'id', 'title', 'description', 'created_at', \
        'preparation_steps',
    list_filter = 'category', 'author', 'is_published', \
        'preparation_steps_is_html',
    list_per_page = 25
    list_editable = 'is_published',
    ordering = '-id',
    prepopulated_fields = {
        'slug': ('title',)
    }
    
    inlines = [
        TagInLine,
    ]
    

admin.site.register(Category, CategoryAdmin)
