# adoptions/admin.py
from django.contrib import admin
from .models import Animal, AdoptionApplication

@admin.register(Animal)
class AnimalAdmin(admin.ModelAdmin):
    list_display = ('name', 'age', 'breed', 'status', 'location')  # Display these fields in the list view
    list_filter = ('status', 'breed')  # Add filters for status and breed
    search_fields = ('name', 'breed', 'location')  # Add search functionality
    fields = ('name', 'age', 'breed', 'race', 'description', 'image', 'location', 'latitude', 'longitude', 'status')  # Fields to display in the form

@admin.register(AdoptionApplication)
class AdoptionApplicationAdmin(admin.ModelAdmin):
    list_display = ('animal', 'applicant_name', 'applicant_email', 'applied_at')
    search_fields = ('animal__name', 'applicant_name', 'applicant_email')
