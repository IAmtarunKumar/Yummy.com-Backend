# tasks/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.user_register, name='user_register'),
    path('login/', views.user_login, name='user_login'),
    path('logout/', views.user_logout, name='user_logout'),

    path('data/', views.data, name='data'),
    path('community/get/', views.list_communities, name='showCommunity'),
    path('community/post/', views.create_community, name='postCommunity'),
    path('my_recipe/get/', views.showRecipe, name='recipe_get'),
    path('my_recipe/post/', views.addRecipe, name='Create_Recipe'),

    path('search/', views.chat_gpt, name='chat_gpt'),

    path('custom/', views.custom_recipe, name='cumtom_recipe'),



    # path('recipe/', views.RecipeListCreateView.as_view),





    # path('recipe/', views.showRecipe, name='showRecipe'),
    # path('addRecipe/', views.addRecipe, name='addRecipe'),
]
