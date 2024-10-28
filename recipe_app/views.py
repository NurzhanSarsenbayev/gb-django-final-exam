import random
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from .models import Recipe,Ingredient,Category
from .forms import *
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
# Create your views here.

import logging

logger = logging.getLogger(__name__)

def some_view(request):
    logger.debug('This is a debug message.')

class SignUp(CreateView):
  form_class = UserCreationForm
  success_url = reverse_lazy('login')
  template_name = 'registration/signup.html'

class CustomLoginView(FormView):
    template_name = 'registration/login.html'
    form_class = AuthenticationForm
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        login(self.request, form.get_user())
        return super().form_valid(form)

@login_required
def logout_view(request):
    logout(request)
    return redirect('home')  # Redirect to home after logout

@login_required
def home(request):
  all_recipes = Recipe.objects.all()

  # Randomly select 5 recipes if more than 5 exist
  recipe_count = all_recipes.count()
  if recipe_count > 5:
    random_recipes = random.sample(list(all_recipes), 5)  # Random selection
  else:
    random_recipes = all_recipes  # If fewer than 5, just take all available recipes

  #Pass the recipes to the template
  context = {'recipes': random_recipes}
  return render(request, 'recipe_app/home.html', context)

def custom_error_view(request, status):
  if status == 404:
    template_name = '500.html'
  elif status == 500:
    template_name = '500.html'
  else:
    template_name = 'generic_error.html'  # Fallback for other errors

  return render(request, template_name, status=status)

def wrong_user_error(request):
  return render(request, 'recipe_app/wrong_user_error.html', status=403)


# Tested for error screen
#def test_error_view(request):
  #raise Exception("This is a test exception for 500 error handling.")

class RecipeList(ListView):
  model = Recipe
  template_name = 'recipe_app/recipe_list.html'

class RecipeDetail(DetailView):
  model = Recipe
  template_name = 'recipe_app/recipe_detail.html'
  context_object_name = 'recipe'

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    # Add comments and the comment form to the context
    context['comments'] = self.object.comments.all()
    context['form'] = CommentForm()
    return context

  def post(self, request, *args, **kwargs):
    # Use get_object() to retrieve the recipe for adding the comment
    self.object = self.get_object()
    form = CommentForm(request.POST)

    if form.is_valid():
      comment = form.save(commit=False)
      comment.recipe = self.object  # Associate the comment with the recipe
      comment.author = self.request.user  # Associate the comment with the logged-in user
      comment.save()
      return redirect('recipe_detail', pk=self.object.pk)

  # If the form is not valid, re-render with errors
    context = self.get_context_data(form=form)
    return self.render_to_response(context)

class RecipeCreate(LoginRequiredMixin, CreateView):  # Ensure user is logged in
  model = Recipe
  form_class = RecipeCreateForm
  template_name = 'recipe_app/recipe_create_form.html'

  def form_valid(self, form):
    # Debugging statements
    print("User is authenticated:", self.request.user.is_authenticated)
    print("User:", self.request.user)

    recipe = form.save(commit=False)  # Do not save yet


    recipe.author = self.request.user  # Use the logged-in user


    recipe.save()  # Now save the recipe instance

    # Handle Many-to-Many relationships
    categories = form.cleaned_data['categories']
    ingredients = form.cleaned_data['ingredients']

    # Set selected categories and ingredients
    recipe.categories.set(categories)
    recipe.ingredients.set(ingredients)

    # Handle new categories
    new_categories = form.cleaned_data.get('new_categories')
    if new_categories:
      categories_list = [cat.strip() for cat in new_categories.split(',')]
      for cat in categories_list:
        category_obj, created = Category.objects.get_or_create(name=cat)
        recipe.categories.add(category_obj)

    # Handle new ingredients
    new_ingredients = form.cleaned_data.get('new_ingredients')
    if new_ingredients:
      ingredients_list = [ing.strip() for ing in new_ingredients.split(',')]
      for ing in ingredients_list:
        ingredient_obj, created = Ingredient.objects.get_or_create(name=ing)
        recipe.ingredients.add(ingredient_obj)

    return redirect('recipe_detail', pk=recipe.pk)  # Redirect to the recipe detail page

  def form_invalid(self, form):
    # This will print form errors to the console for debugging
    print("Form is invalid!")
    print(form.errors)
    return super().form_invalid(form)


class RecipeUpdate(LoginRequiredMixin, UpdateView):
  model = Recipe
  fields = ['title', 'description', 'process', 'cooking_time', 'image', 'ingredients', 'categories']
  template_name = 'recipe_app/recipe_update_form.html'

  def dispatch(self, request, *args, **kwargs):
    recipe = self.get_object()
    # Check if the user is the author of the recipe
    if recipe.author != request.user:
      return redirect('wrong_user_error')
    return super().dispatch(request, *args, **kwargs)

  def get_success_url(self):
    return reverse_lazy('recipe_detail', args=[self.object.pk])


class RecipeDelete(DeleteView):
  model = Recipe
  template_name = 'recipe_app/recipe_delete_form.html'
  success_url = reverse_lazy('home')  # Redirect to home after deletion

  def dispatch(self, request, *args, **kwargs):
    recipe = self.get_object()
    # Check if the user is the author of the recipe
    if recipe.author != request.user:
      return redirect('wrong_user_error')  # Redirect to your custom error page
    return super().dispatch(request, *args, **kwargs)

class IngredientList(ListView):
  model = Ingredient
  template_name = 'recipe_app/ingredient_list.html'

class IngredientCreate(CreateView):
  model = Ingredient
  template_name = 'recipe_app/ingredient_create_form.html'
  fields = '__all__'

class IngredientUpdate(UpdateView):
  model = Ingredient
  template_name = 'recipe_app/ingredient_update_form.html'
  fields = '__all__'

class IngredientDelete(DeleteView):
  model = Ingredient
  template_name = 'recipe_app/ingredient_delete_form.html'
  success_url = reverse_lazy('ingredient_list')

class CategoryList(ListView):
    model = Category
    template_name = 'recipe_app/category_list.html'
    context_object_name = 'categories'


# Show all recipes for a specific category
class CategoryDetail(DetailView):
  model = Category
  template_name = 'recipe_app/category_detail.html'
  context_object_name = 'category'

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    category = self.object
    # Get all recipes for the selected category
    context['recipes'] = Recipe.objects.filter(categories=category)
    return context

class CategoryUpdate(UpdateView):
  model = Category
  template_name = 'recipe_app/category_update_form.html'
  fields = '__all__'

class CategoryDelete(DeleteView):
  model = Category
  template_name = 'recipe_app/category_delete_form.html'
  success_url = reverse_lazy('category_list')

# class RecipeCategoryList(ListView):
#   model = RecipeCategory
#   template_name = 'recipe_app/recipeCategory_list.html'
#
# class RecipeCategoryCreate(CreateView):
#   model = RecipeCategory
#   template_name = 'recipe_app/recipeCategory_create_form.html'
#   fields = '__all__'
#
# class RecipeCategoryUpdate(UpdateView):
#   model = RecipeCategory
#   template_name = 'recipe_app/recipeCategory_update_form.html'
#   fields = '__all__'
#
# class RecipeCategoryDelete(DeleteView):
#   model = RecipeCategory
#   template_name = 'recipe_app/recipeCategory_delete_form.html'
#   success_url = reverse_lazy('recipeCategory_list')