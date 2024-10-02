from django import forms

from .models import *


class RecipeCreateForm(forms.ModelForm):
    categories = forms.ModelMultipleChoiceField(
        queryset=Category.objects.all(),
        widget=forms.CheckboxSelectMultiple,  # Can be changed to SelectMultiple for a dropdown
        required=False,
        label="Select Categories"
    )
    ingredients = forms.ModelMultipleChoiceField(
        queryset=Ingredient.objects.all(),
        widget=forms.CheckboxSelectMultiple,  # Can be changed to SelectMultiple for a dropdown
        required=False,
        label="Select Ingredients"
    )


    # Fields for adding new categories and ingredients
    new_categories = forms.CharField(required=False,
                                     label='Add new categories (comma-separated)',
                                     widget=forms.TextInput(attrs={'placeholder': 'e.g., Dessert, Vegan'}))
    new_ingredients = forms.CharField(required=False,
                                      label='Add new ingredients (comma-separated)',
                                      widget=forms.TextInput(attrs={'placeholder': 'e.g., Sugar, Flour'}))
    class Meta:
        model = Recipe
        fields = ['title', 'description', 'process', 'cooking_time', 'image']

    def save(self, commit=True):
        # Save the basic Recipe object (without M2M fields)
        recipe = super().save(commit=False)
        # Save the recipe to assign an ID
        recipe.save()

        # Initialize empty lists for categories and ingredients
        all_categories = []
        all_ingredients = []

        # Handle existing selected categories
        selected_categories = self.cleaned_data.get('categories')
        if selected_categories:
            all_categories.extend(selected_categories)  # Add selected categories to the list

        # Handle new category creation
        new_categories = self.cleaned_data.get('new_categories')
        if new_categories:
            categories_list = [cat.strip() for cat in new_categories.split(',')]
            for cat in categories_list:
                category_obj, created = Category.objects.get_or_create(name=cat)
                all_categories.append(category_obj)  # Add new category to the list

        # Set all categories (existing + new) at once
        if all_categories:
            recipe.categories.set(all_categories)

        # Handle existing selected ingredients
        selected_ingredients = self.cleaned_data.get('ingredients')
        if selected_ingredients:
            all_ingredients.extend(selected_ingredients)  # Add selected ingredients to the list

        # Handle new ingredient creation
        new_ingredients = self.cleaned_data.get('new_ingredients')
        if new_ingredients:
            ingredients_list = [ing.strip() for ing in new_ingredients.split(',')]
            for ing in ingredients_list:
                ingredient_obj, created = Ingredient.objects.get_or_create(name=ing)
                all_ingredients.append(ingredient_obj)  # Add new ingredient to the list

        # Set all ingredients (existing + new) at once
        if all_ingredients:
            recipe.ingredients.set(all_ingredients)

        # Save M2M relationships if commit is True
        if commit:
            recipe.save()  # Ensure the recipe instance is saved
            self.save_m2m()  # Handle any additional M2M relations, if necessary

        return recipe

class IngredientCreateForm(forms.ModelForm):
    class Meta:
        model = Ingredient
        fields = '__all__'

# class RecipeCategoryCreateForm(forms.ModelForm):
#     class Meta:
#         model = RecipeCategory
#         fields = '__all__'

class CategoryCreateForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = '__all__'


class RecipeUpdateForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ['title', 'description', 'process', 'cooking_time', 'image',]

class IngredientUpdateForm(forms.ModelForm):
    class Meta:
        model = Ingredient
        fields = '__all__'

# class RecipeCategoryUpdateForm(forms.ModelForm):
#     class Meta:
#         model = RecipeCategory
#         fields = '__all__'

class CategoryUpdateForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = '__all__'

