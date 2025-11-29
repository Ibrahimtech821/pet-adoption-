from django.urls import path
from django.contrib import admin
from .views import MyLoginView,home,about,register , filter_pets, pet_detail,submit_adoption_request, adoption_success

urlpatterns= [
    path('',home,name="home"),
    path('login/', MyLoginView.as_view(), name='login'),
    path('register/',register,name='register'),
    path('home',home,name='home'),
    path('about/', about, name='about'),
    path('pets/', filter_pets, name='pets_list'),
    path('pets/<int:pet_id>/', pet_detail, name='pet_detail'),
    path('adopt/<int:pet_id>/', submit_adoption_request, name='submit_adoption'),
    path('adoption-success/', adoption_success, name='adoption_success'),
    

]
