from django.conf import settings
from django.urls import reverse

from django.db import models
from django.contrib.auth.models import User


# Create your models here.


class Recipe(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    process = models.TextField()
    cooking_time = models.IntegerField(help_text='Time in minutes')
    image = models.ImageField(upload_to='recipe_images', null=True, blank=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,null=True, blank=True)
    ingredients = models.ManyToManyField('Ingredient', related_name='recipes')  # Changed to ManyToMany
    categories = models.ManyToManyField('Category', related_name='recipes')  # Changed to ManyToMany
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        # Capitalize the category name before saving
        self.title = self.title.capitalize()
        super(Recipe, self).save(*args, **kwargs)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('recipe_detail', args=[self.pk])

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True,)

    def save(self, *args, **kwargs):
        # Capitalize the category name before saving
        self.name = self.name.capitalize()
        super(Category, self).save(*args, **kwargs)

    def __str__(self):
        return self.name

class Ingredient(models.Model):

    name = models.CharField(max_length=100, unique=True)

    def save(self, *args, **kwargs):
        # Capitalize the category name before saving
        self.name = self.name.capitalize()
        super(Ingredient, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


'''
TODO At this point, I don't believe this model is useful. 
I tried various versions (both with ForeignKey and M2M relations),
neither seem to logically fit into app workflow.
'''
# class RecipeCategory(models.Model):
#     recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
#     category = models.ManyToManyField('Category', through='RecipeCategory', related_name='recipes')
#     main_ingredient = models.ManyToManyField('Ingredient', through='RecipeCategory', related_name='recipes')
#     def __str__(self):
#         return str(self.recipe)

