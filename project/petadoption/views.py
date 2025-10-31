from django.shortcuts import render,HttpResponse,redirect
from .models import enterpets
from django.contrib.auth.views import LoginView
from django.views.generic.edit import CreateView
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.contrib.auth import login

class MyLoginView(LoginView):
    template_name = 'login.html'         
    redirect_authenticated_user = True    
    next_page='/home'


def register(request):
    new_user=UserCreationForm()
    if request.method=='POST':
        new_user=UserCreationForm(data=request.POST)
        if new_user.is_valid():
            user=new_user.save()
            login(request,user)
            return redirect('login')
        return render(request,'register.html',{"register":new_user})

def home(request):
    return HttpResponse("hello")
def view(request):
    pets=enterpets.objects.all()
    return render(request,"pets_data.html",{"data":pets})
def about(request):
    return render(request,"about.html")
