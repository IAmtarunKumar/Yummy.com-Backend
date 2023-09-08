from rest_framework import serializers
from .models import Community,Recipe

class CommunitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Community
        fields = '__all__'  # Serialize all fields in the Community model


class RecipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Community
        fields = '__all__'  # Serialize all fields in the Community model


