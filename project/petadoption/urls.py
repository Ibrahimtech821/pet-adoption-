from django.urls import path
from django.contrib import admin
from .views import MyLoginView,home,about,register

urlpatterns= [
    path('',home,name="home"),
    path('login/', MyLoginView.as_view(), name='login'),
    path('register/',register,name='register'),
    path('home',home,name='home'),
    

]
