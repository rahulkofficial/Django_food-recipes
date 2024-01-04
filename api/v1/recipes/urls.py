from django.urls import path
from api.v1.recipes import views

urlpatterns = [
    path('', views.recipes),
    path('/details/<int:id>', views.recipeDetail),
    path('/add', views.add_recipe),
    path('/update/<int:id>', views.update_recipe),
    path('/delete/<int:id>', views.delete_recipe),
    path('/categories', views.categories),
    path('/add_fav/<int:id>', views.add_fav),
    path('/remove_fav/<int:id>', views.remove_fav),
    path('/fav', views.fav),
]