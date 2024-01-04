from django.urls import path

from web import views

app_name="web"
urlpatterns = [
    path('',views.main,name="main"),
    path('login',views.login,name="login"),
    path('logout',views.logout,name='logout'),
    path('signup',views.signup,name="signup"),
    path('recipes',views.recipes,name="recipes"),
    path('recipes_detailed/<int:id>',views.recipes_detailed,name="recipes_detailed"),
    path('add',views.add,name="add"),
    path('recipes_detailed/update/<int:id>',views.update,name="update"),
    path('recipes_detailed/delete/<int:id>',views.delete,name="delete"),
    path('add_fav/<int:id>',views.add_fav,name="add_fav"),
    path('remove_fav/<int:id>',views.remove_fav,name="remove_fav"),
    path('favs',views.favs,name="favs"),
]