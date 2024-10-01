from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy

# Create your views here.
from .models import Recipe,RecipeCategory,Ingredient,Category
from .forms import *
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm


class SignUp(CreateView):
  form_class = UserCreationForm
  success_url = reverse_lazy('login')
  template_name = 'registration/signup.html'

# Custom Login View
class CustomLoginView(FormView):
    template_name = 'registration/login.html'
    form_class = AuthenticationForm
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        login(self.request, form.get_user())
        return super().form_valid(form)

# Custom Logout View
@login_required
def logout_view(request):
    logout(request)
    return redirect('home')  # Redirect to home after logout

@login_required
def home(request):
  context = {"name": request.user}
  return render(request, "recipe_app/home.html", context)

class RecipeList(ListView):
  model = Recipe
  template_name = 'recipe_app/recipe_list.html'

class RecipeDetail(DetailView):
  model = Recipe
  template_name = 'recipe_app/recipe_detail.html'
  context_object_name = 'recipe'

class RecipeCreate(CreateView):
  model = Recipe
  template_name = 'recipe_app/recipe_create_form.html'
  fields = '__all__'

class RecipeUpdate(UpdateView):
  model = Recipe
  template_name = 'recipe_app/recipe_update_form.html'
  fields = '__all__'

class RecipeDelete(DeleteView):
  model = Recipe
  template_name = 'recipe_app/recipe_delete_form.html'
  success_url = reverse_lazy('recipe_list')

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

class CategoryCreate(CreateView):
  model = Category
  template_name = 'recipe_app/category_create_form.html'
  fields = '__all__'

class CategoryUpdate(UpdateView):
  model = Category
  template_name = 'recipe_app/category_update_form.html'
  fields = '__all__'

class CategoryDelete(DeleteView):
  model = Category
  template_name = 'recipe_app/category_delete_form.html'
  success_url = reverse_lazy('category_list')

class RecipeCategoryList(ListView):
  model = RecipeCategory
  template_name = 'recipe_app/recipeCategory_list.html'

class RecipeCategoryCreate(CreateView):
  model = RecipeCategory
  template_name = 'recipe_app/recipeCategory_create_form.html'
  fields = '__all__'

class RecipeCategoryUpdate(UpdateView):
  model = RecipeCategory
  template_name = 'recipe_app/recipeCategory_update_form.html'
  fields = '__all__'

class RecipeCategoryDelete(DeleteView):
  model = RecipeCategory
  template_name = 'recipe_app/recipeCategory_delete_form.html'
  success_url = reverse_lazy('recipeCategory_list')