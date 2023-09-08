from django.db import models

# Create your models here.


class User(models.Model):
    user_id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    password = models.TextField()
    added_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name + '--' + self.username


class Recipe(models.Model):
    recipe_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=200)
    ingredients = models.TextField()
    instructions = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

class Community(models.Model):
    community_id = models.AutoField(primary_key=True)
    description = models.TextField()
   
    def __str__(self):
        return self.description