
from django.db import models
from django.contrib.auth import get_user_model
from phonenumber_field.modelfields import PhoneNumberField
import uuid

User = get_user_model()

# Create your models here.
class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True, null=True)
    id_user = models.IntegerField()
    profileimg = models.ImageField(upload_to='profile_images', default='avatar.jpg')
    phonenumber = PhoneNumberField(blank=True, null=True) 
    location = models.CharField(max_length=100,blank=True, null=True)
    job = models.CharField(max_length=120,blank=True, null=True)
    twitter = models.CharField(max_length=100,blank=True, null=True)
    instagram = models.CharField(max_length=100,blank=True, null=True)
    facebook = models.CharField(max_length=100,blank=True, null=True)
    youtube = models.CharField(max_length=100,blank=True, null=True)
    
    def __str__(self):
        return self.user.username

class Tag(models.Model):
    name = models.CharField(max_length=150)
    
    
    def __str__(self):
        return self.name  
    
class Recipe(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    title = models.CharField(max_length=150)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='recipe_images', default='r.jpg')
    video_url = models.URLField(blank=True,null=True)
    tag = models.ManyToManyField(Tag)
    directions = models.JSONField(blank=True,null=True)
    ingredients = models.JSONField(blank=True,null=True)
    nutritions = models.JSONField(blank=True,null=True)
    people = models.IntegerField(default=0)
    cooktime = models.IntegerField(default=0)
    ingredient_total = models.IntegerField(default=0)
    date_created = models.DateTimeField(auto_now_add=True)
    views = models.IntegerField(default=0)
    
    def __str__(self):
        return self.title
    
class Comment(models.Model):
    recipe = models.ForeignKey(Recipe,related_name="comments",on_delete=models.CASCADE)
    user = models.CharField(max_length=150)
    profileimg = models.ImageField(upload_to='comment_images')
    body = models.TextField(blank=True, null=True)
    date_added = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.recipe.title
    
class Rating(models.Model):
    recipe = models.ForeignKey(Recipe,related_name="ratings",on_delete=models.CASCADE)
    score = models.IntegerField(default=0)
    
    def __str__(self):
        return self.recipe.title
    
    

    