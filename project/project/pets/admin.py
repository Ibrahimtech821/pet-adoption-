from django.contrib import admin
from .models import Pet


@admin.register(Pet)
class PetAdmin(admin.ModelAdmin):
    list_display = ['name', 'species', 'breed', 'age', 'size', 'location', 'created_at']
    list_filter = ['species', 'size', 'gender', 'vaccinated', 'neutered']
    search_fields = ['name', 'breed', 'location']
    ordering = ['-created_at']
