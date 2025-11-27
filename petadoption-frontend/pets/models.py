from django.db import models


class Pet(models.Model):
    SPECIES_CHOICES = [
        ('dog', 'Dog'),
        ('cat', 'Cat'),
    ]
    
    SIZE_CHOICES = [
        ('small', 'Small'),
        ('medium', 'Medium'),
        ('large', 'Large'),
    ]
    
    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
    ]
    
    name = models.CharField(max_length=100)
    species = models.CharField(max_length=10, choices=SPECIES_CHOICES)
    breed = models.CharField(max_length=100)
    age = models.IntegerField()
    size = models.CharField(max_length=10, choices=SIZE_CHOICES)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    location = models.CharField(max_length=200)
    image = models.URLField()
    description = models.TextField()
    personality = models.JSONField(default=list)  # Store as JSON array
    medical_history = models.TextField()
    vaccinated = models.BooleanField(default=False)
    neutered = models.BooleanField(default=False)
    good_with_kids = models.BooleanField(default=False)
    good_with_pets = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.name} - {self.breed}"
    
    def get_personality_display(self):
        """Return personality traits as comma-separated string"""
        return ', '.join(self.personality) if self.personality else ''
