# tasks/views.py
from django.contrib.auth import authenticate, login, logout 



from django.contrib.auth.models import User
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from rest_framework.authtoken.models import Token  # Import Token model
from rest_framework.decorators import authentication_classes, permission_classes, api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from django.contrib.auth.decorators import login_required
from rest_framework.parsers import JSONParser

import openai
from django.conf import settings

from .models import Community, Recipe, User

# convert queryset to json
from .serializer import CommunitySerializer, RecipeSerializer

# register


@csrf_exempt
def user_register(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            email = data.get('email')
            username = data.get('username')
            password = data.get('password')

        

            if not email or not username or not password:
                return JsonResponse({'error': 'Missing required fields'}, status=400)

            # Check if the username or email already exists
            if User.objects.filter(username=username).exists() or User.objects.filter(email=email).exists():
                return JsonResponse({'error': 'Username or email already exists'}, status=400)

            # Create a new custom user
            user = User.objects.create(email=email,username=username, password=password)
            # Set the user's password
            user.save()  # Save the user object

            return JsonResponse({'message': 'User registered successfully'})
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON data'}, status=400)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)
# login
@csrf_exempt
def user_login(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data['username']
        password = data['password']
        # user = authenticate(request, username=username, password=password)
        user=User.objects.filter(username=username).exists() and User.objects.filter(password=password).exists()
        if user:
            # login(request, user)
            # Generate or retrieve an existing token for the user
            # token, created = Token.objects.get_or_create(user=user)
            # return JsonResponse({'message': 'Login successful', 'token': token.key , "username":username})
            return JsonResponse({'message': 'Login successful', 'token': "login" , "username":username})

        else:
            return JsonResponse({'message': 'Invalid credentials'}, status=401)

# Logout Route
@csrf_exempt
def user_logout(request):
    if request.method == 'POST':
        logout(request)
        return JsonResponse({'message': 'Logout successful'})

# protected route


@csrf_exempt
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
@login_required
def data(request):
    if request.method == 'GET':

        return JsonResponse({'message': 'Protected data accessed successfully'})
    else:
        return JsonResponse({"msg": "please login first"})


# Get a list of all communities
@csrf_exempt
def list_communities(request):
    if request.method == 'GET':
        communities = Community.objects.all()
        serializer = CommunitySerializer(communities, many=True)
        return JsonResponse(serializer.data, safe=False)
    else:
        return JsonResponse({'message': 'Invalid request method'}, status=400)


# Create a new community
# @csrf_exempt
# @api_view(['POST'])
# @authentication_classes([TokenAuthentication])
# @permission_classes([IsAuthenticated])
# @login_required
@csrf_exempt
# @authentication_classes([TokenAuthentication])
# @permission_classes([IsAuthenticated])
def create_community(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        description = data.get('description')
        community = Community(description=description)
        community.save()
        return JsonResponse({'message': 'Community created successfully'}, status=201)
    else:
        return JsonResponse({'message': 'Invalid request method'}, status=400)


@csrf_exempt
# @permission_classes([IsAuthenticated])
@api_view(['GET'])
def showRecipe(request):
    if request.method == 'GET':
        tasks = Recipe.objects.all()
        recipe_list = [{'user_id': recipes.user_id,  'title': recipes.title, 'ingredients': recipes.ingredients,
                        'instructions': recipes.instructions} for recipes in tasks]
        return JsonResponse(recipe_list, safe=False)


@csrf_exempt
def addRecipe(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        user_id = data.get('user_id')  # Get user_id from the request data
        title = data.get('title')
        ingredients = data.get('ingredients')
        instructions = data.get('instructions')

        try:
            # Check if the user with the provided user_id exists
            user = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return JsonResponse({'message': 'User does not exist'}, status=400)

        # Create and save the Recipe instance with the valid user_id
        recipe = Recipe(user=user, title=title, ingredients=ingredients, instructions=instructions)
        recipe.save()

        return JsonResponse({'message': 'Recipe posted successfully'}, status=201 )

    return JsonResponse({'message': 'Invalid request method'}, status=400)


@csrf_exempt
def chat_gpt(request):
    if request.method == 'POST':
        # Parse JSON data from the request body
        try:
            data = json.loads(request.body)
            keyword = data.get('keyword')
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON data'}, status=400)
        # Set up OpenAI API key
        openai.api_key = settings.OPENAI_API_KEY
        # Make a request to OpenAI GPT-3 API
        try:
           
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{ "role": "user",
                            "content": f'Create 4 recipes in JSON format using the keyword "{keyword}". Each recipe should have the following structure: "title": "Recipe Title", "ingredients": "Array of ingredients ", "instructions": "Array of Cooking steps instructions"  output in json format only.' + "Example : [{} , {} , {}]" }
  ])
            if response.choices:
                data=response.choices[0].message.content
                new_data = json.loads(data)
            else:
                return JsonResponse({'error': 'No response from GPT-3'}, status=500)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
        return JsonResponse({'gpt3_output': new_data}, status=201)
    return JsonResponse({'error': 'Invalid request method'}, status=405)





@csrf_exempt
def demo(request):
    if request.method == 'POST':
        # Parse JSON data from the request body
        try:
            data = json.loads(request.body)
            keyword = data.get('keyword')
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON data'}, status=400)
        # Set up OpenAI API key
        openai.api_key = settings.OPENAI_API_KEY
        # Make a request to OpenAI GPT-3 API
        try:
           
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{ "role": "user",
                            "content": f'Create 4 recipes in JSON format using the keyword "{keyword}". Each recipe should have the following structure: "title": "Recipe Title", "ingredients": "Array of ingredients ", "instructions": "Array of Cooking steps instructions"  output in json format only.' + "Example : [{} , {} , {}]" }
  ])
            if response.choices:
                data=response.choices[0].message.content
                new_data = json.loads(data)
            else:
                return JsonResponse({'error': 'No response from GPT-3'}, status=500)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
        return JsonResponse({'gpt3_output': new_data}, status=201)
    return JsonResponse({'error': 'Invalid request method'}, status=405)






# @csrf_exempt
# def custom_recipe(request):
#     if request.method == 'POST':
#         # Parse JSON data from the request body
#         try:
#             data = json.loads(request.body)

            
#             cuisines = data.get('cuisines')
#             ingredients_not = data.get('ingredients_not')
#             skills = data.get('skills')
#             allergies = data.get('allergies')
#             follow_diets = data.get('follow_diets')

#         except json.JSONDecodeError:
#             return JsonResponse({'error': 'Invalid JSON data'}, status=400)
#         # Set up OpenAI API key
#         openai.api_key = settings.OPENAI_API_KEY
#         # Make a request to OpenAI GPT-3 API
#         try:
           
#             response = openai.ChatCompletion.create(
#                 model="gpt-3.5-turbo",
#                 messages=[{ "role": "user",
#                          "content": f"Create 5 recipes in JSON format based on your preferences. You mentioned the following: - Cuisines: {cuisines} - Ingredients to avoid: {ingredients_not} - Cooking skills: {skills} - Allergies: {allergies} - Specific diets: {follow_diets} For each recipe, provide the following structure:  - 'title': 'Recipe Title'  - 'ingredients': 'Array of ingredients ' - 'instructions': 'Array of cooking instructions steps' Output the recipes in JSON format as a list of dictionaries." + " Example: [{}, {}, {}, {}, {}]" }
#   ])
#             if response.choices:
#                 data=response.choices[0].message.content
#                 print(data)
#                 new_data = json.loads(data)
#             else:
#                 return JsonResponse({'error': 'No response from GPT-3'}, status=500)
#         except Exception as e:
#             return JsonResponse({'error': str(e)}, status=500)
#         return JsonResponse({'gpt3_output': new_data}, status=201)
#     return JsonResponse({'error': 'Invalid request method'}, status=405)

