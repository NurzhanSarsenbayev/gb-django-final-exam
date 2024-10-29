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

    def like_count(self):
        return self.likes.count()

    def favorite_count(self):
        return self.favorites.count()

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

class Comment(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='comments',null=True, blank=True)
    recipe = models.ForeignKey(Recipe,on_delete=models.CASCADE,related_name='comments')
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Comment by {self.author.username if self.author else "Unknown"} on {self.recipe.title}'

class Like(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='likes',null=True, blank=True)
    recipe = models.ForeignKey(Recipe,on_delete=models.CASCADE,related_name='likes')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('author', 'recipe')
    def __str__(self):
        return f'{self.author} like {self.recipe}'


class Favorite(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='favorites',null=True, blank=True)
    recipe = models.ForeignKey(Recipe,on_delete=models.CASCADE,related_name='favorites')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('author', 'recipe')
    def __str__(self):
        return f'{self.author} favorite like {self.recipe}'


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

