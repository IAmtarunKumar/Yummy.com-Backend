# tasks/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('api/signin/', views.user_register, name='user_register'),
    path('api/login/', views.user_login, name='user_login'),
    path('api/logout/', views.user_logout, name='user_logout'),

    path('data/', views.data, name='data'),

    path('api/get/community/', views.list_communities, name='showCommunity'),
    path('api/post/community/', views.create_community, name='postCommunity'),


    path('api/get/my_recipe/', views.showRecipe, name='recipe_get'),
    path('api/post/my_recipe/', views.addRecipe, name='Create_Recipe'),

    path('api/search/dish/', views.chat_gpt, name='chat_gpt'),

    path('api/filtered/dish/', views.custom_recipe, name='cumtom_recipe'),



    # path('recipe/', views.RecipeListCreateView.as_view),





    # path('recipe/', views.showRecipe, name='showRecipe'),
    # path('addRecipe/', views.addRecipe, name='addRecipe'),
]
