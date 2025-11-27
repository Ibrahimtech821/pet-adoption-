from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from .models import Pet


def home(request):
    """Home page view"""
    featured_pets = Pet.objects.all()[:3]
    context = {
        'featured_pets': featured_pets,
    }
    return render(request, 'pets/home.html', context)


def pet_list(request):
    """List all pets with filtering"""
    pets = Pet.objects.all()
    
    # Get filter parameters
    search = request.GET.get('search', '')
    species = request.GET.get('species', '')
    size = request.GET.get('size', '')
    age_range = request.GET.get('age', '')
    
    # Apply filters
    if search:
        pets = pets.filter(name__icontains=search) | pets.filter(breed__icontains=search)
    
    if species:
        pets = pets.filter(species=species)
    
    if size:
        pets = pets.filter(size=size)
    
    if age_range:
        if age_range == 'young':
            pets = pets.filter(age__lte=2)
        elif age_range == 'adult':
            pets = pets.filter(age__gte=3, age__lte=7)
        elif age_range == 'senior':
            pets = pets.filter(age__gte=8)
    
    context = {
        'pets': pets,
        'search': search,
        'selected_species': species,
        'selected_size': size,
        'selected_age': age_range,
    }
    return render(request, 'pets/pet_list.html', context)


def pet_detail(request, pet_id):
    """Pet detail page"""
    pet = get_object_or_404(Pet, id=pet_id)
    context = {
        'pet': pet,
    }
    return render(request, 'pets/pet_detail.html', context)


def about(request):
    """About page view"""
    return render(request, 'pets/about.html')


def contact(request):
    """Contact page view"""
    return render(request, 'pets/contact.html')


def submit_adoption(request):
    """Handle adoption form submission (AJAX)"""
    if request.method == 'POST':
        # In a real application, you would process the form data here
        # For now, just return success
        return JsonResponse({'success': True, 'message': 'Application submitted successfully!'})
    return JsonResponse({'success': False, 'message': 'Invalid request method'})
