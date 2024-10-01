from django.contrib import admin
from recipe_app.models import *
# Register your models here.

admin.site.register(Recipe)
admin.site.register(Ingredient)
admin.site.register(Category)
admin.site.register(RecipeCategory)