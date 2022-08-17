from django.urls import path

from . import views

urlpatterns = [
    path('',views.index,name='index'),
    path('add',views.add,name='add'),
    path('edit/<str:pk>/',views.edit,name='edit'),
    path('login',views.login,name='login'),
    path('logout',views.logout,name='logout'),
    path('register',views.register,name='register'),
    path('profile/<str:pk>/',views.profile,name='profile'),
    path('recipe/<str:pk>/',views.recipe,name='recipe'),
    path('recipes',views.recipes,name='recipes'),
    path('settings',views.settings,name='settings'),
    path('category/<str:tag>/',views.category,name='category'),
    path('search',views.search,name='search'),
    path('delete/<str:pk>',views.delete,name='delete'),
    path('deleteComment/<str:pk>/',views.deleteComment,name='deleteComment'),
]
