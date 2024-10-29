from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views
from django.conf.urls import handler500

handler404 = lambda request, exception: views.custom_error_view(request, 404)
handler500 = lambda request: views.custom_error_view(request, 500)
urlpatterns = [
    path('', views.home, name='home'),
    path('signup/', views.SignUp.as_view(), name='signup'),
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('recipes/', views.RecipeList.as_view(), name='recipe_list'),
    path('recipes/<int:pk>/', views.RecipeDetail.as_view(), name='recipe_detail'),
    path('recipes/create/', views.RecipeCreate.as_view(), name='recipe_create'),
    path('recipes/<int:pk>/update/', views.RecipeUpdate.as_view(), name='recipe_update'),
    path('recipes/<int:pk>/delete/', views.RecipeDelete.as_view(), name='recipe_delete'),
    path('categories/', views.CategoryList.as_view(), name='category_list'),
    path('categories/<int:pk>/', views.CategoryDetail.as_view(), name='category_detail'),
    path('wrong_user_error/', views.wrong_user_error, name='wrong_user_error'),
    #path('test-error/', views.test_error_view, name='test_error'),
    path('recipe/<int:recipe_id>/like/', views.toggle_like, name='toggle_like'),
    path('recipe/<int:recipe_id>/favorite/', views.toggle_favorite, name='toggle_favorite'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)