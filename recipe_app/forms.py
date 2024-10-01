from django import forms

from .models import *

class RecipeCreateForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = '__all__'

class IngredientCreateForm(forms.ModelForm):
    class Meta:
        model = Ingredient
        fields = '__all__'

class RecipeCategoryCreateForm(forms.ModelForm):
    class Meta:
        model = RecipeCategory
        fields = '__all__'

class CategoryCreateForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = '__all__'


class RecipeUpdateForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = '__all__'

class IngredientUpdateForm(forms.ModelForm):
    class Meta:
        model = Ingredient
        fields = '__all__'

class RecipeCategoryUpdateForm(forms.ModelForm):
    class Meta:
        model = RecipeCategory
        fields = '__all__'

class CategoryUpdateForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = '__all__'

