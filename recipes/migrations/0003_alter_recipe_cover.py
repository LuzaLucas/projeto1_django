# Generated by Django 5.0.3 on 2024-03-14 17:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0002_alter_recipe_category_alter_recipe_cover'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipe',
            name='cover',
            field=models.ImageField(blank=True, default=None, null=True, upload_to='recipes/covers/%Y/%m/%d/'),
        ),
    ]
