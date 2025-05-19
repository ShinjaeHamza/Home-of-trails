from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from geopy.geocoders import Nominatim
from django.contrib.messages import add_message, constants as messages
from django.utils.timezone import now
from django.contrib.auth.models import User

class Animal(models.Model):
    ADOPTION_STATUS = (
        ('available', 'Available'),
        ('pending', 'Pending'),
        ('adopted', 'Adopted'),
    )

    name = models.CharField(max_length=100)
    age = models.IntegerField()
    breed = models.CharField(max_length=100)
    race = models.CharField(max_length=100, blank=True, null=True)
    description = models.TextField()
    image = models.ImageField(upload_to='animals/', blank=True, null=True)
    location = models.CharField(max_length=255, default='Unknown Location')
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)
    status = models.CharField(max_length=10, choices=ADOPTION_STATUS, default='available')
    date_added = models.DateTimeField(default=timezone.now)

    def save(self, *args, **kwargs):
        # Automatically fetch latitude and longitude if location is provided
        if self.location and (not self.latitude or not self.longitude):
            geolocator = Nominatim(user_agent="animal_adoption")
            location = geolocator.geocode(self.location)
            if location:
                self.latitude = location.latitude
                self.longitude = location.longitude
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


from django.contrib.auth.models import User

class AdoptionApplication(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]

    animal = models.ForeignKey(Animal, on_delete=models.CASCADE, related_name='applications')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='adoption_applications')  # Add this field
    applicant_name = models.CharField(max_length=100)
    applicant_email = models.EmailField()
    message = models.TextField()
    applied_at = models.DateTimeField(default=timezone.now)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')

    def __str__(self):
        return f"Application for {self.animal.name} by {self.applicant_name}"



# Signal to update the animal's status when an application is approved@receiver(post_save, sender=AdoptionApplication)
def notify_user_on_status_change(sender, instance, **kwargs):
    # Check if the status has changed
    if instance.status == 'approved':
        # Notify the user about approval
        add_message(instance.applicant_email, messages.SUCCESS, f"Your adoption application for {instance.animal.name} has been approved!")
    elif instance.status == 'rejected':
        # Notify the user about rejection
        add_message(instance.applicant_email, messages.ERROR, f"Your adoption application for {instance.animal.name} has been rejected.")

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"


# Signal to create or update the user profile
@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.get_or_create(user=instance)
    else:
        if hasattr(instance, 'profile'):
            instance.profile.save()
            
class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=now)  # Use the imported 'now' function

    def __str__(self):
        return f"Notification for {self.user.username}: {self.message}"

    @property
    def unread_count(self):
        return Notification.objects.filter(user=self.user, is_read=False).count()