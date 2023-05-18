from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import CustomUser, UserProfile


# @receiver(post_save, sender=CustomUser)
# def create_user_profile(sender, instance, created, **kwargs):
#     if created:
#         UserProfile.objects.create(user=instance)

@receiver(post_save, sender=CustomUser)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        # Create the UserProfile instance
        user_profile = UserProfile.objects.create(user=instance)

        # Get the corresponding country for the city
        if instance.city and instance.city.country:
            user_profile.country = instance.city.country
            user_profile.save()
