from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import AdoptionApplication, Notification
from django.contrib.auth.models import User


@receiver(post_save, sender=AdoptionApplication)
def notify_user_on_status_change(sender, instance, **kwargs):
    if instance.status == 'approved':
        Notification.objects.create(
            user=instance.user,
            message=f"Your adoption application for {instance.animal.name} has been approved!"
        )
    elif instance.status == 'rejected':
        Notification.objects.create(
            user=instance.user,
            message=f"Your adoption application for {instance.animal.name} has been rejected."
        )

    # OPTIONAL: If you still want to notify an admin or system user like 'petfinder'
    try:
        system_user = User.objects.get(username='petfinder')
        Notification.objects.create(
            user=system_user,
            message=f"A decision has been made on an application for {instance.animal.name}."
        )
    except User.DoesNotExist:
        pass  # Or log a warning
