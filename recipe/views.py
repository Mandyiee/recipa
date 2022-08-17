from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.models import User, auth
from django.db.models import Avg
from django.db.models import Count
from django.db.models.functions import Length
from django.contrib.auth.decorators import login_required

from recipe.models import Comment, Profile, Recipe, Tag, Rating

def index(request):
    trend = Recipe.objects.order_by('-views').first()
    trending = Recipe.objects.order_by('-date_created')[:3]
    popularlist = Recipe.objects.order_by('-views')[:4]
    entertaining = Recipe.objects.all().annotate(con=Count('comments')).order_by('-con').distinct()[:4]
    context = {
        'trend':trend,
        'trending':trending,
        'popularlist':popularlist,
        'entertaining':entertaining
    }
    return render(request,'index.html',context)

@login_required(login_url='login')
def add(request):
    if request.method == 'POST':
        user_id = User.objects.get(username = request.user.username)
        user = Profile.objects.get(user= user_id.id)
        title = request.POST['title']
        description = request.POST['description']
        image = request.FILES.get('image')
        video_url = request.POST['video_url'] 
        cooktime = request.POST['cooktime']
        people = request.POST['people']
        tags = request.POST.getlist('tag')
        directions = request.POST.getlist('directions')
        ingredient_name = request.POST.getlist('ingredient_name')
        ingredient_amount = request.POST.getlist('ingredient_amount')
        nutrition_name= request.POST.getlist('nutrition_name')
        nutrition_amount= request.POST.getlist('nutrition_amount')
        ingredient_total = len(ingredient_name)
       
        dirObj = {
            'direction': directions
        }
        ingobjarr = []
        for i in range(len(ingredient_amount)):
            ingobjarr.append({ingredient_name[i]:ingredient_amount[i]})
            
        ingObj = {
            'ingredient' : ingobjarr
        }
        nutobjarr = []
        for i in range(len(nutrition_amount)):
            nutobjarr.append({nutrition_name[i]:nutrition_amount[i]})
        nutObj = {
            'nutrition' : nutobjarr
        }
        
        recipe = Recipe.objects.create(user=user,title=title,description=description,image=image,video_url=video_url,cooktime=cooktime,people=people,directions=dirObj,nutritions=nutObj,ingredients=ingObj,ingredient_total=ingredient_total)
        for tag in tags:
            tagModel, created = Tag.objects.get_or_create(name=tag)
            recipe.tag.add(tagModel.id)
        recipe.save()
        return redirect('recipe/' + str(recipe.id))
    return render(request,'add-recipe.html')


def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        first_name =  request.POST['first_name']
        last_name =  request.POST['last_name']
        email = request.POST['email']
        password  = request.POST['password']
        password2  = request.POST['password2']
        
        if password == password2:
            if User.objects.filter(username=username).exists():
                messages.info(request, 'Username Taken')
                return redirect('register')
            elif User.objects.filter(email=email).exists():
                messages.info(request, 'Email Taken')
                return redirect('register')
            else:
                user = User.objects.create_user(username=username,email=email,password=password,first_name=first_name,last_name=last_name)
                
                user.save()
                
                user_login = auth.authenticate(username=username,password=password)
                auth.login(request, user_login)
                
                user_model = User.objects.get(username=username)
                profile = Profile.objects.create(user=user_model,id_user=user_model.id)
                profile.save()
                return redirect('settings')
        else:
            messages.info(request, 'Password does not match')
            return redirect('register')
            
    return render(request,'register.html')

def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        
        user = auth.authenticate(username=username,password=password)
        
        if user is not None:
            auth.login(request,user)
            return redirect('index')
        else:
            messages.info(request, 'Credentials Invalid')
            return redirect('login')
    return render(request,'login.html')

@login_required(login_url='login')
def settings(request):
    user_profile = Profile.objects.get(user=request.user)
    if request.method == 'POST':
        if request.FILES.get('image') == None:
            image = user_profile.profileimg
            bio = request.POST['bio']
            location = request.POST['location']
            phonenumber = request.POST['phonenumber']
            twitter = request.POST['twitter']
            facebook = request.POST['facebook']
            instagram = request.POST['instagram'] 
            youtube = request.POST['youtube']
            job = request.POST['job']
            
            user_profile.profileimg = image
            user_profile.bio = bio
            user_profile.youtube = youtube
            user_profile.job = job
            user_profile.location = location
            user_profile.phonenumber = phonenumber
            user_profile.twitter = twitter
            user_profile.facebook = facebook
            user_profile.instagram = instagram 
            
            user_profile.save()
        if request.FILES.get('image') != None:
            image = request.FILES.get('image')
            bio = request.POST['bio']
            location = request.POST['location']
            phonenumber = request.POST['phonenumber']
            twitter = request.POST['twitter']
            facebook = request.POST['facebook']
            instagram = request.POST['instagram'] 
            
            user_profile.youtube = youtube
            user_profile.job = job
            user_profile.profileimg = image
            user_profile.bio = bio
            user_profile.location = location
            user_profile.phonenumber = phonenumber
            user_profile.twitter = twitter
            user_profile.facebook = facebook
            user_profile.instagram = instagram 
            
            user_profile.save()
            
        return redirect('/profile/' + request.user.username)
            
    return render(request,'settings.html',{'user_profile':user_profile})

def profile(request,pk):
    profile = Profile.objects.get(user__username=pk)
    recipes = Recipe.objects.filter(user=profile)
    return render(request,'profile.html',{'profile':profile,'recipes':recipes})

def recipe(request,pk):
    recipe = Recipe.objects.get(id=pk)
    user = User.objects.get(username=recipe.user)
    profile = Profile.objects.get(user=user)
    recipe.views += 1
    recipe.save()
    
    ratings = Rating.objects.filter(recipe=recipe)
    rating = Rating.objects.filter(recipe=recipe).count()
    rating_avg = ratings.aggregate(Avg('score'))
    tags = recipe.tag.all()
    likes = Recipe.objects.none()
    tag_id = []
    for tag in tags:
        like =  Recipe.objects.filter(tag=tag)
        tag_id.append(tag.id)
    likes = Recipe.objects.filter(tag__id__in=tag_id).distinct().exclude(id=pk)[:3]
   
    
    
    if request.method == 'POST':
        name = request.user.username
        profileimg = Profile.objects.get(user__username=request.user.username).profileimg
        body = request.POST['body']
        score = request.POST['rating']
        if body == "":
            newRating = Rating.objects.create(recipe=recipe,score=score)
            newRating.save()
        else:    
            newComment = Comment.objects.create(user=name,profileimg=profileimg,body=body,recipe=recipe)
            newComment.save()
            newRating = Rating.objects.create(recipe=recipe,score=score)
            newRating.save()
        
    
    return render(request,'recipe.html',{'recipe':recipe,'profile':profile,'rating':rating,'rating_avg':rating_avg,'likes':likes})

def recipes(request):
    recipes = Recipe.objects.all()
    return render(request,'recipes.html',{'recipes':recipes})

def category(request,tag):
    tag = Tag.objects.get(name=tag)
    recipes = Recipe.objects.filter(tag=tag)
    return render(request,'category.html',{'recipes':recipes})

def search(request):
    recipes = None
    if request.method == 'POST':
        opt = request.POST['search-opt']
        value = request.POST['search-value']
        
        if opt == 'recipe':
            recipes = Recipe.objects.filter(title__icontains=value)
            
        elif opt == 'tag':
            tag = Tag.objects.filter(name__icontains=value)
            
            tag_id = tag.values_list('id', flat=True)
            tag_ids = list(tag_id)[0]
            tags = Tag.objects.get(id=tag_ids)
            recipes = Recipe.objects.filter(tag=tag_ids)
            
            
        else:
            recipes = Recipe.objects.filter(user__user__username__icontains=value)

            
    return render(request,'search.html',{'recipes':recipes})

@login_required(login_url='login')
def edit(request,pk):
    recipeModel = Recipe.objects.get(id=pk)
    
    if request.method == 'POST':
        user_id = User.objects.get(username = request.user.username)
        user = Profile.objects.get(user= user_id.id)
        title = request.POST['title']
        description = request.POST['description']
        image = request.FILES.get('image') or recipeModel.image
        video_url = request.POST['video_url'] 
        cooktime = request.POST['cooktime']
        people = request.POST['people']
        tags = request.POST.getlist('tag')
        directions = request.POST.getlist('directions')
        ingredient_name = request.POST.getlist('ingredient_name')
        ingredient_amount = request.POST.getlist('ingredient_amount')
        nutrition_name= request.POST.getlist('nutrition_name')
        nutrition_amount= request.POST.getlist('nutrition_amount')
        ingredient_total = len(ingredient_name)
       
        dirObj = {
            'direction': directions
        }
        ingobjarr = []
        for i in range(len(ingredient_amount)):
            ingobjarr.append({ingredient_name[i]:ingredient_amount[i]})
            
        ingObj = {
            'ingredient' : ingobjarr
        }
        nutobjarr = []
        for i in range(len(nutrition_amount)):
            nutobjarr.append({nutrition_name[i]:nutrition_amount[i]})
        nutObj = {
            'nutrition' : nutobjarr
        }
        recipeModel.user=user
        recipeModel.title=title
        recipeModel.description=description
        recipeModel.image=image
        recipeModel.video_url=video_url
        recipeModel.cooktime=cooktime
        recipeModel.people=people
        recipeModel.directions=dirObj
        recipeModel.nutritions=nutObj
        recipeModel.ingredients=ingObj
        recipeModel.ingredient_total=ingredient_total
        
        for tag in tags:
            tagModel, created = Tag.objects.get_or_create(name=tag)
            recipeModel.tag.add(tagModel.id)
        recipeModel.save()
        return redirect('/recipe/' + str(recipeModel.id))
    return render(request,'edit.html',{'recipe':recipeModel})

@login_required(login_url='login')
def delete(request,pk):
    recipeModel = Recipe.objects.get(id=pk)
    recipeModel.delete()
    return redirect('recipes')

@login_required(login_url='login')
def deleteComment(request,pk):
    comment = Comment.objects.get(id=pk)
    comment.delete()
    recipe = comment.recipe
    return redirect('recipe/' + str(recipe.id))
        
@login_required(login_url='login')
def logout(request):
    auth.logout(request)
    return redirect('login')


def error_404_view(request, exception):
    return render(request, 'not-found.html')