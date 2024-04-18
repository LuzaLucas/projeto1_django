from django.contrib import admin
from .models import Category, Recipe


class CategoryAdmin(admin.ModelAdmin):
    ...


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
    autocomplete_fields = 'tags',
    

admin.site.register(Category, CategoryAdmin)
