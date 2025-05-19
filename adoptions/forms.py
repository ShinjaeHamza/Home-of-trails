# adoptions/forms.py
from django import forms
from .models import AdoptionApplication
from .models import Profile
from .models import Animal
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Notification

class AdoptionApplicationForm(forms.ModelForm):
    class Meta:
         model = AdoptionApplication  # Specify the model
         fields = ['message']  # Include only the 'message' field
         widgets = {
            'message': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 5,
                'placeholder': 'Why do you want to adopt this pet?'
            }),
        }
class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['bio', 'profile_picture']

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['bio', 'profile_picture', 'phone_number', 'address']


class AnimalForm(forms.ModelForm):
    class Meta:
        model = Animal
        fields = ['name', 'breed', 'race', 'age', 'status','location', 'image']
        
class CustomUserCreationForm(UserCreationForm):
    full_name = forms.CharField(max_length=100, required=True, help_text="Required. Enter your full name.")
    email = forms.EmailField(required=True, help_text="Required. Enter a valid email address.")
    phone_number = forms.CharField(max_length=15, required=False, help_text="Optional. Enter your phone number.")
    address = forms.CharField(max_length=255, required=False, help_text="Optional. Enter your address or city.")

    class Meta:
        model = User
        fields = ['username', 'full_name', 'email', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        # Create a Profile instance with additional fields
        profile = Profile.objects.create(
            user=user,
            phone_number=self.cleaned_data.get('phone_number'),
            address=self.cleaned_data.get('address'),
        )
        # If you are creating a Notification, ensure the user is assigned correctly
        # Example:
        # Notification.objects.create(
        #     user=user,  # Assign the User instance
        #     message="Welcome to the platform!"
        # )
        return user
    
def some_view(request):
    user = User.objects.get(username='petfinder')  # Ensure this fetches a valid User instance
    Notification.objects.create(
        user=user,  # Assign the User instance
        message="Your request has been approved."
    )