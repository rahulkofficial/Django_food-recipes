from rest_framework.response import Response
from rest_framework.decorators import api_view,permission_classes
from rest_framework.permissions import IsAuthenticated,AllowAny

from web.models import Recipes,Categories,Favorites
from django.shortcuts import get_object_or_404
from api.v1.recipes.serializers import RecipeSerializer,CategorySerializer,FavSerializer


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def recipes(request):
    instances=Recipes.objects.all()
    q=request.GET.get("q")
    value=request.GET.get("v")
    if q:
        instances=instances.filter(title__icontains=q)
    context={
        "request":request
    }
    if value:
        cate=Categories.objects.filter(title=value)
        instances=instances.filter(category=cate[0])
    serializer=RecipeSerializer(instances,many=True,context=context,)
    response_data={
        "status":6000,
        "data":serializer.data
    }
    return Response(response_data)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def categories(request):
    instances=Categories.objects.all()
    context={
        "request":request
    }
    serializer=CategorySerializer(instances,many=True,context=context,)
    response_data={
        "status":6000,
        "data":serializer.data
    }
    return Response(response_data)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def recipeDetail(request,id):
    if Recipes.objects.filter(id=id).exists():
        instance=Recipes.objects.get(id=id)
        context={
            "request":request
        }
        serializer=RecipeSerializer(instance,context=context)
        response_data={
            "status":6000,
            "data":serializer.data
        }
        return Response(response_data)
    else:
        response_data={
            "status":6001,
            "message":"recipe not exist"
        }
        return Response(response_data)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def add_recipe(request):
    current_user=request.user
    title=request.data['title']
    file=request.data['file']
    description=request.data['description']
    category=request.data['category']
    recipe=Recipes(title=title,description=description,image=file,user=current_user,category=category)
    cat=Categories(title=category)
    if not Recipes.objects.filter(title=title,description=description,image=file,user=current_user,category=category).exists():
        if recipe and cat:
            recipe.save()
            if not Categories.objects.filter(title=category).exists():
                cat.save()
            response_data={
                "status":6000,
                "message":"Successfully added recipe"
            }
            return Response(response_data)
        else:
            response_data={
                "status":6001,
                "message":"Error"
            }
            return Response(response_data)

    else:
        response_data={
                "status":6001,
                "message":"already exists"
            }
        return Response(response_data)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def update_recipe(request,id):
    category=request.data['category']
    instance = get_object_or_404(Recipes, id=id)
    serializer = RecipeSerializer(instance, data=request.data, partial=True)
    if serializer.is_valid():
        if 'file' in request.data:
            if request.data['file']:
                instance.image.delete()
                instance.image = request.data['file']
            instance.title=request.data['title']
            instance.category=request.data['category']
            instance.description=request.data['description']
            instance.save()
            if not Categories.objects.filter(title=category).exists():
                Categories(title=category).save()
            response_data={
                "status":6000,
                "message":"Successfully updated recipe"
            }
            return Response(response_data)
        else:
            response_data={
                "status":6001,
                "message":"file not found"
            }
            return Response(response_data)
    else:
        response_data={
            "status":6001,
            "message":"Error"
        }
        return Response(response_data)
    

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def delete_recipe(request,id):
    recipe=Recipes.objects.filter(id=id)
    if recipe:
        recipe.delete()
        response_data={
            "status":6000,
            "message":"Successfully deleted recipe"
        }
        return Response(response_data)
    else:
        response_data={
            "status":6001,
            "message":"Error"
        }
        return Response(response_data)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def add_fav(request,id):
    recipe=Recipes.objects.filter(id=id)
    current_user=request.user
    fav=Favorites(user=current_user,recipe=recipe[0],is_fav=True)
    if not Favorites.objects.filter(user=current_user,recipe=recipe[0]).exists():
        if fav:
            fav.save()
            response_data={
                "status":6000,
                "message":"Successfully added to favorite"
            }
            return Response(response_data)
        else:
            response_data={
                "status":6001,
                "message":"Error"
            }
            return Response(response_data)
    else:
        response_data={
            "status":6001,
            "message":"already exists"
        }  
        return Response(response_data)
        


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def remove_fav(request,id):
    recipe=Recipes.objects.filter(id=id)
    current_user=request.user
    fav=Favorites.objects.filter(user=current_user,recipe=recipe[0])
    if fav:
        fav.delete()
        response_data={
            "status":6000,
            "message":"Successfully removed from favorite"
        }
        return Response(response_data)
    else:
        response_data={
            "status":6001,
            "message":"Error"
        }
        return Response(response_data)
    

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def fav(request):
    instances=Favorites.objects.all()
    context={
        "request":request
    }
    serializer=FavSerializer(instances,many=True,context=context,)
    response_data={
        "status":6000,
        "data":serializer.data
    }
    return Response(response_data)