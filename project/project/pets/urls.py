from django.urls import path
from . import views

app_name = 'pets'

urlpatterns = [
    path('', views.home, name='home'),
    path('pets/', views.pet_list, name='pet_list'),
    path('pets/<int:pet_id>/', views.pet_detail, name='pet_detail'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('submit-adoption/', views.submit_adoption, name='submit_adoption'),
]
