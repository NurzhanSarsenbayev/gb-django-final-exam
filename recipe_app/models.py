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
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    ingredients = models.TextField()
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
class RecipeCategory(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    category = models.ManyToManyField(Category)
    main_ingredient = models.ManyToManyField(Ingredient)

    def __str__(self):
        return str(self.recipe)

