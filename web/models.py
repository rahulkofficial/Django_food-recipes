from django.db import models
from django.contrib.auth.models import User


class Categories(models.Model):
    title=models.CharField(max_length=225)

    class Meta:
        db_table="web_categories"
        verbose_name_plural="categories"
    
    def __str__(self):
        return self.title


class Recipes(models.Model):
    title=models.CharField(max_length=225)
    description=models.TextField()
    image=models.ImageField(upload_to="rimage/",blank=True)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    category=models.CharField(max_length=225)

    class Meta:
        db_table="web_recipes"
        verbose_name_plural="recipes"

    def __str__(self):
        return str(self.id)
    


class Favorites(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    recipe=models.ForeignKey(Recipes,on_delete=models.CASCADE)
    is_fav=models.BooleanField(default=False)

    class Meta:
        db_table="web_favorite"
        verbose_name_plural="favorites"
