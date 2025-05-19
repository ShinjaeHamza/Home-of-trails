from django.shortcuts import render

# Create your views here.

# adoptions/views.py
# adoptions/views.

from django.shortcuts import render, get_object_or_404, redirect
from .models import Animal, AdoptionApplication
from .forms import AdoptionApplicationForm
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import logout
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .forms import ProfileForm
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Profile
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from .models import AdoptionApplication
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect
from .forms import ProfileUpdateForm
from django.http import JsonResponse
from .forms import CustomUserCreationForm
from .models import Animal
from .models import Notification
from django.core.paginator import Paginator


def animal_list(request):
    # Get search and filter parameters from the request
    search_query = request.GET.get('search', '')  # Search by name or breed
    breed_filter = request.GET.get('breed', '')  # Filter by breed
    race_filter = request.GET.get('race', '')  # Filter by race
    status_filter = request.GET.get('status', '')  # Filter by status

    # Start with all animals
    animals = Animal.objects.all()

    # Apply search filter
    if search_query:
        animals = animals.filter(
            name__icontains=search_query
        ) | animals.filter(
            breed__icontains=search_query
        )

    # Apply additional filters
    if breed_filter:
        animals = animals.filter(breed__icontains=breed_filter)
    if race_filter:
        animals = animals.filter(race__icontains=race_filter)
    if status_filter:
        animals = animals.filter(status__iexact=status_filter)

    # Pass the filtered animals and current filters to the template
    return render(request, 'adoptions/animal_list.html', {
        'animals': animals,
        'search_query': search_query,
        'breed_filter': breed_filter,
        'race_filter': race_filter,
        'status_filter': status_filter,
    })
def animal_detail(request, pk):
    animal = get_object_or_404(Animal, pk=pk)
    applications = animal.applications.all()
    return render(request, 'adoptions/animal_detail.html', {
        'animal': animal,
        'applications': applications,
        'latitude': animal.latitude,
        'longitude': animal.longitude,
    })

@login_required
def apply_adoption(request, pk):
    animal = get_object_or_404(Animal, pk=pk)

    # Prevent applying if the animal is already adopted
    if animal.status == "adopted":
        messages.error(request, "This pet has already been adopted.")
        return redirect('animal_detail', pk=animal.pk)

    if request.method == 'POST':
        form = AdoptionApplicationForm(request.POST)
        if form.is_valid():
            application = form.save(commit=False)
            application.animal = animal
            application.user = request.user  # Assign the logged-in user to the application
            application.applicant_name = request.user.get_full_name() or request.user.username
            application.applicant_email = request.user.email
            application.save()
            messages.success(request, "Your adoption application has been submitted!")
            return redirect('animal_detail', pk=animal.pk)
    else:
        form = AdoptionApplicationForm()

    return render(request, 'adoptions/apply_adoption.html', {'form': form, 'animal': animal})
def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Explicitly create the Profile
            Profile.objects.create(user=user)
            login(request, user)  # Log the user in after registration
            messages.success(request, 'Registration successful!')
            return redirect('home')
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

def custom_logout(request):
    logout(request)
    return render(request, 'registration/logout.html')

@login_required
def profile(request):
    profile = request.user.profile  # Assuming a one-to-one relationship with the User model
    form = ProfileForm(instance=profile)

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('profile')

    return render(request, 'registration/profile.html', {'form': form})

def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    else:
        instance.profile.save()
def user_dashboard(request):
    applications = AdoptionApplication.objects.filter(applicant_email=request.user.email)
    return render(request, 'adoptions/user_dashboard.html', {'applications': applications})

def withdraw_application(request, pk):
    application = get_object_or_404(AdoptionApplication, pk=pk, applicant_email=request.user.email)
    if application.status == 'pending':
        application.delete()
    return redirect('user_dashboard')

def custom_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                # Check if the user is a superuser
                if user.is_superuser:
                    return redirect('/admin/')  # Redirect to the admin page
                else:
                    return redirect('animal_list')  # Redirect normal users to the homepage
    else:
        form = AuthenticationForm()
    return render(request, 'registration/login.html', {'form': form})
def animal_list(request):
    # Get search and filter parameters from the request
    breed_filter = request.GET.get('breed', '').strip()
    race_filter = request.GET.get('race', '').strip()
    status_filter = request.GET.get('status', '').strip()

    # Start with all animals
    animals = Animal.objects.all()

    # Apply filters
    if breed_filter:
        animals = animals.filter(breed__icontains=breed_filter)
    if race_filter:
        animals = animals.filter(race__icontains=race_filter)
    if status_filter:
        animals = animals.filter(status=status_filter)
    # Pagination
    paginator = Paginator(animals, 6)  # Show 6 animals per page
    page_number = request.GET.get('page')
    animals = paginator.get_page(page_number)

    # Pass filters back to the template for persistence
    context = {
        'animals': animals,
        'breed_filter': breed_filter,
        'race_filter': race_filter,
        'status_filter': status_filter,
    }
    return render(request, 'adoptions/animal_list.html', context)
def approve_application(request, pk):
    application = get_object_or_404(AdoptionApplication, pk=pk)
    application.status = 'approved'
    application.save()
    return redirect('application_list')

def reject_application(request, pk):
    application = get_object_or_404(AdoptionApplication, pk=pk)
    application.status = 'rejected'
    application.save()
    return redirect('application_list')
def update_profile(request):
    profile = request.user.profile
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = ProfileUpdateForm(instance=profile)
    return render(request, 'adoptions/update_profile.html', {'form': form})

from django.shortcuts import render
from .models import Animal

def main_page(request):
    # Filter animals to exclude those with the status "adopted"
    animals = Animal.objects.filter(status='available')[:3]  # Show only the first 3 animals initially
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':  # Check if it's an AJAX request
        offset = int(request.GET.get('offset', 0))
        animals = Animal.objects.filter(status='available')[offset:offset + 3]
        animal_data = [
            {
                'name': animal.name,
                'breed': animal.breed,
                'age': animal.age,
                'status': animal.status,
                'image_url': animal.image.url,
                'detail_url': f'/adoptions/{animal.pk}/'
            }
            for animal in animals
        ]
        return JsonResponse({'animals': animal_data})
    return render(request, 'main_page.html', {'animals': animals})
def dashboard(request):
    return render(request, 'adoptions/dashboard.html')

def profile_view(request):
    # Example: Display notifications on the profile page
    return render(request, 'registration/profile.html', {
        'messages': messages.get_messages(request),
    })
@login_required
def notifications_view(request):
    notifications = Notification.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'adoptions/notifications.html', {'notifications': notifications})

@login_required
def application_list(request):
    applications = AdoptionApplication.objects.filter(applicant_name=request.user.username).order_by('-applied_at')
    return render(request, 'adoptions/application_list.html', {'applications': applications})

