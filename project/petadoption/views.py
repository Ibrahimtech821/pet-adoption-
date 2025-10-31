from django.shortcuts import render,HttpResponse,redirect , get_object_or_404
from .models import enterpets , adoptionform
from django.contrib.auth.views import LoginView
from django.views.generic.edit import CreateView
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import adoption as AdoptionForm


class MyLoginView(LoginView):
    template_name = 'login.html'         
    redirect_authenticated_user = True    
    next_page='/home'


def register(request):  ##user login 
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
def view_pets(request):
    pets=enterpets.objects.all()
    return render(request,"pets_data.html",{"data":pets})
def about(request):
    return render(request,"about.html")


def filter_pets(request):
    pet_specie = request.GET.get('specie', '')
    pet_color = request.GET.get('color', '')
    pet_breed = request.GET.get('breed', '')
    pet_age = request.GET.get('Age', '')

    pets = enterpets.objects.all()
    error = ''
    if pet_specie:
        pets = pets.filter(specie__iexact=pet_specie)
    if pet_color:
        pets = pets.filter(color__iexact=pet_color)
    if pet_breed:
        pets = pets.filter(breed__icontains=pet_breed)
    if pet_age:
        try:
            age_int = int(pet_age) #from string to int
            pets = pets.filter(Age=age_int)
        except ValueError:
            error = "Invalid age input. Please enter a number."

    if not pets.exists():
        error = "No pets found matching your search criteria."

    return render(request, 'petadoption/pets_list.html', {
        'pets': pets,
        'filter_specie': pet_specie,
        'filter_color': pet_color,
        'filter_breed': pet_breed,
        'error': error
    })


def pet_detail(request, pet_id):
    pet = get_object_or_404(enterpets, id=pet_id)
    pet_data = {
        'name': pet.pet_name,
        'age': pet.Age if pet.Age else 'Unknown',  
        'specie': pet.specie if pet.specie else 'Unknown',
        'breed': pet.breed if pet.breed else 'Unknown',
        'color': pet.color if pet.color else 'Unknown',
        'description': pet.description if pet.description else '',
        'any_injuries': pet.any_injuries if pet.any_injuries else 'No',
        'injury_description': pet.describe_if_of_injury_if_there if pet.describe_if_of_injury_if_there else 'There are no injuries',
    }
    return render(request, 'petadoption/pet_detail.html', {'pet': pet_data})

#requires login
@login_required(login_url='/login/')
def submit_adoption_request(request, pet_id=None):
    pet = None
    if pet_id:
        pet = get_object_or_404(enterpets, id=pet_id)

    if request.method == 'POST': #user submitted
        form = AdoptionForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Adoption request submitted successfully.")
            return redirect('adoption_success')
    else: #just opened the page
        form = AdoptionForm()

    return render(request, 'petadoption/adoption_form.html', {'form': form, 'pet': pet})

def adoption_success(request):
    return render(request, 'petadoption/adoption_success.html')



def search_pets(request):
    search_name = request.GET.get('name', '')
    if search_name:
        pets = enterpets.objects.filter(pet_name__icontains=search_name)
        if not pets.exists():
            error = f"No pets found with the name '{search_name}'"
        else: #if there is a result , no error
            error = ''
    else:
        pets = enterpets.objects.all() #if empty show all pets
        error = ''

    return render(request, 'petadoption/pets_list.html', {
        'pets': pets,
        'error': error
    })

