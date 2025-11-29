from django.urls import path
from django.contrib import admin
from .views import MyLoginView,home,about,register,pet_detail,submit_adoption_request, adoption_success,pet_quiz,my_requests,logout_user, pets_view

urlpatterns= [
    path('',home,name="home"),
    path('login/', MyLoginView.as_view(), name='login'),
    path('register/',register,name='register'),
    path('home',home,name='home'),
    path('about/', about, name='about'),
    path('pets/', pets_view, name='pets'),
    path('pets/<int:pet_id>/', pet_detail, name='pet_detail'),
    path('adopt/<int:pet_id>/', submit_adoption_request, name='submit_adoption_request'),
    path('adoption-success/', adoption_success, name='adoption_success'),
    path('quiz/', pet_quiz , name='pet_quiz'),
    path('my_requests/',my_requests, name='my_requests'),
    path('logout/',logout_user, name='logout'),

    

]