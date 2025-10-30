from django.urls import path
from django.contrib import admin
from . import views

urlpatterns= [
    path('',views.members,name='member'),
    path('/admin/',admin.site.urls)

]
