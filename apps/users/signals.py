from django.db.models.signals import post_save
from django.db.models.signals import pre_save
from django.dispatch import receiver
from .models import CustomUser, UserProfile
from django.utils import timezone


@receiver(post_save, sender=CustomUser)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        # Create the UserProfile instance
        user_profile = UserProfile.objects.create(user=instance)

        # Get the corresponding country for the city
        if instance.city and instance.city.country:
            user_profile.country = instance.city.country
            user_profile.save()


@receiver(pre_save, sender=CustomUser)
def update_last_active(sender, instance, **kwargs):
    if instance.is_authenticated:
        try:
            profile = instance.userprofile
        except UserProfile.DoesNotExist:
            profile = UserProfile(user=instance)
        profile.last_active = timezone.now()
        profile.save()
