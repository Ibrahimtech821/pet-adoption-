from django.shortcuts import render,HttpResponse,redirect , get_object_or_404
from .models import enterpets , adoptionform,PetFood
from django.contrib.auth.views import LoginView
from django.views.generic.edit import CreateView
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.contrib.auth import login,logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import  AdoptionForm,customcreationform
from .otp import generate_otp





class MyLoginView(LoginView):
    template_name = 'login.html'         
    redirect_authenticated_user = True    
    next_page='/home'


def register(request):  ##user login 
    new_user=customcreationform()
    if request.method=='POST':
        new_user=customcreationform(data=request.POST)
        if new_user.is_valid():
            user=new_user.save(commit=False)
            otp=generate_otp(user.email)
            request.session['otp']=otp
            request.session['user_data']=request.POST
            return redirect('verify_otp')
        return render(request,'register.html',{"register":new_user})
    else:  
        new_user = customcreationform()
        return render(request,'register.html',{"register":new_user})
    
def verify_otp(request):
    if request.method=='POST':
        entered_otp=request.POST.get('otp')
        if str(entered_otp)==str(request.session.get('otp')):
            data = request.session.get('user_data')
            form = customcreationform(data)
            if form.is_valid():
                user = form.save()
                login(request, user)
                del request.session['otp']
                del request.session['user_data']
                return redirect('home')
        else:
            error = "Invalid OTP, please try again."
            return render(request, "verify_otp.html", {"error": error})
    return render(request, "verify_otp.html")
    

def logout_user(request):
    logout(request)             
    return redirect('home')


def home(request):
    if request.user.is_authenticated and request.user.is_staff:
        from django.contrib.auth import logout
        logout(request)  
    return render(request, "home.html")


def about(request):
    return render(request,"about.html")


def pets_view(request):
    # Start with all pets
    pets = enterpets.objects.all().order_by('id')
    error = ""

    
    pet_specie = request.GET.get('specie', '')
    pet_color = request.GET.get('color', '')
    pet_breed = request.GET.get('breed', '')
    pet_age = request.GET.get('age_range', '')  

    
    if pet_specie:
        pets = pets.filter(specie__iexact=pet_specie)
    if pet_color:
        pets = pets.filter(color__iexact=pet_color)
    if pet_breed:
        pets = pets.filter(breed__icontains=pet_breed)
    if pet_age:
        try:
            # convert age group to actual age range
            if pet_age == 'young':
                pets = pets.filter(Age__gte=0, Age__lte=2)
            elif pet_age == 'adult':
                pets = pets.filter(Age__gte=3, Age__lte=7)
            elif pet_age == 'senior':
                pets = pets.filter(Age__gte=8)
        except ValueError:
            error = "Invalid age input. Please enter a number."

    return render(request, 'pets.html', {
        'pet': pets,
        'filter_specie': pet_specie,
        'filter_color': pet_color,
        'filter_breed': pet_breed,
        'error': error
    })



def pet_detail(request, pet_id):
    pet = get_object_or_404(enterpets, id=pet_id)
    pet_data = {
        'id': pet.id,
        'name': pet.pet_name,
        'age': pet.Age if pet.Age else 'Unknown',  
        'specie': pet.specie if pet.specie else 'Unknown',
        'breed': pet.breed if pet.breed else 'Unknown',
        'color': pet.color if pet.color else 'Unknown',
        'description': pet.description if pet.description else '',
        'any_injuries': pet.any_injuries if pet.any_injuries else 'No',
        'injury_description': pet.describe_if_of_injury_if_there if pet.describe_if_of_injury_if_there else 'There are no injuries',
        'image': pet.image if pet.image else None,
        'is_adopted': pet.is_adopted,
    }
    return render(request, 'pet_detail.html', {'pet': pet_data})

#requires login
@login_required(login_url='/login/')
def submit_adoption_request(request, pet_id=None):
    pet = None
    if pet_id:
        pet = get_object_or_404(enterpets, id=pet_id)

    if request.method == 'POST': #user submitted
        form = AdoptionForm(request.POST)
        if form.is_valid():
            req=form.save(commit=False)
            req.user=request.user
            if pet:
                req.pet=pet
            req.save()
            messages.success(request, "Adoption request submitted successfully.")
            return redirect('adoption_success')
    else: #just opened the page
        form = AdoptionForm()

    return render(request, 'adoption_form.html', {'form': form, 'pet': pet})

def adoption_success(request):
    return render(request, 'adoption_success.html')

def my_requests(request):
    submissons=adoptionform.objects.filter(user=request.user)
    return render(request,'view_submission.html',{'submissons':submissons})


def search_pets(request):
    search_name = request.GET.get('name', '').strip()  # Get the search term from the query parameters
    if search_name:
        pets = enterpets.objects.filter(pet_name__icontains=search_name)
        if not pets.exists():
            error = f"No pets found with the name '{search_name}'"
        else: #if there is a result , no error
            error = ''
    else:
        pets = enterpets.objects.all() #if empty show all pets
        error = ''

    return render(request, 'pets.html', {
        'pet': pets,
        'error': error
    })


def pet_quiz(request): 
    scores = {"Dog": 0, "Cat": 0, "Turtle": 0, "Bird": 0, "Rabbit": 0}
    errors = {} # to track empty questiosn
    if request.method == "POST":
        activity = request.POST.get("activity")
        space = request.POST.get("space")
        allergy = request.POST.get("allergy")
        time_avail = request.POST.get("time")
        interactive = request.POST.get("interactive")
        noise = request.POST.get("noise")
        long_life = request.POST.get("long_life")
        kids = request.POST.get("kids")

        for feild_name, field_value in [("activity", activity), ("space", space), ("allergy", allergy), ("time", time_avail), ("interactive", interactive), ("noise", noise), ("long_life", long_life), ("kids", kids)]:
            if not field_value:
                errors[feild_name] = True


        if not errors:
            if activity == "low":
                scores["Cat"] += 3
                scores["Turtle"] += 3
                scores["Rabbit"] += 1
            elif activity == "medium":
                scores["Cat"] += 2
                scores["Bird"] += 2
            elif activity == "high":
                scores["Dog"] += 4

            if space == "small":
                scores["Cat"] += 3
                scores["Turtle"] += 2
            elif space == "medium":
                scores["Cat"] += 2
                scores["Bird"] += 2
                scores["Dog"] += 2
            elif space == "large":
                scores["Dog"] += 4
                scores["Bird"] += 2

            if allergy == "yes":
                scores["Turtle"] += 4
                scores["Rabbit"] += 1  
            else:
                scores["Dog"] += 2
                scores["Cat"] += 2
                scores["Bird"] += 1

            if time_avail == "low":
                scores["Turtle"] += 4
            elif time_avail == "medium":
                scores["Cat"] += 2
                scores["Bird"] += 2
            elif time_avail == "high":
                scores["Dog"] += 4

            if interactive == "yes":
                scores["Dog"] += 4
                scores["Cat"] += 3
                scores["Bird"] += 3
            elif interactive == "no":
                scores["Turtle"] += 4

            if noise == "I don't mind":  
                scores["Dog"] += 3
                scores["Cat"] += 2
                scores["Bird"] += 2
            elif noise == "quiet":
                scores["Turtle"] += 4

            if long_life == "yes":
                scores["Bird"] += 3
                scores["Turtle"] += 3
            elif long_life == "no":
                scores["Dog"] += 1
                scores["Cat"] += 1

            if kids == "yes":
                scores["Dog"] += 3
                scores["Cat"] += 2
                scores["Rabbit"] += 2

            ##save in session to redirect
            request.session['Scores'] = scores
            return redirect('pet_quiz_result')
        
        return render(request, "pet_quiz.html", {"Scores": scores , "errors": errors})
    return render(request, "pet_quiz.html", {"Scores": scores , "errors": errors}) ##get response , empty quiz
    

def pet_quiz_result(request):
    scores = request.session.get('Scores')
    if not scores:
        return redirect('pet_quiz') 
    
    max_score = max(scores.values())
    top_pets = [pet for pet, score in scores.items() if score == max_score]
    return render(request, "pet_quiz_result.html", {"Scores": scores, "top_pets": top_pets})


def petfood_list(request):
    foods = PetFood.objects.all()
    return render(request, 'petfood.html', {'foods': foods})