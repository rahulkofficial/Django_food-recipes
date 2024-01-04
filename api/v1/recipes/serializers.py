from rest_framework import serializers

from web.models import Recipes,Categories,Favorites


class RecipeSerializer(serializers.ModelSerializer):
    class Meta:
        model=Recipes
        fields=['id','title','description','image','category','user']


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model=Categories
        fields=['id','title']


class FavSerializer(serializers.ModelSerializer):
    class Meta:
        model=Favorites
        fields=['id','user','recipe','is_fav']