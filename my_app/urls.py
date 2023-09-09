# tasks/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.user_register, name='user_register'),
    path('login/', views.user_login, name='user_login'),
    path('logout/', views.user_logout, name='user_logout'),

    path('data/', views.data, name='data'),
    path('community/show/', views.list_communities, name='showCommunity'),
    path('com/', views.create_community, name='postCommunity'),
    path('my_recipe/', views.showRecipe, name='recipe_get'),
    path('recipe_create/', views.addRecipe, name='Create_Recipe'),

    path('gpt/', views.chat_gpt, name='chat_gpt'),

    path('custom_recipe/', views.custom_recipe, name='cumtom_recipe'),

    path('demo/', views.demo, name='demo'),




    # path('recipe/', views.RecipeListCreateView.as_view),





    # path('recipe/', views.showRecipe, name='showRecipe'),
    # path('addRecipe/', views.addRecipe, name='addRecipe'),
]
