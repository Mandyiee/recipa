from cProfile import Profile
from django.contrib import admin
from .models import Comment, Profile, Rating, Recipe, Tag
# Register your models here.
admin.site.register(Profile)
admin.site.register(Recipe)
admin.site.register(Comment)
admin.site.register(Tag)
admin.site.register(Rating)