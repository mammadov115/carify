from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import CustomUser, BuyerProfile, DealerProfile


@receiver(post_save, sender=CustomUser)
def create_user_profile(sender, instance, created, **kwargs):
    """
    Automatically create a profile for the user after a new CustomUser is created.
    If role is 'buyer' → BuyerProfile
    If role is 'dealer' → DealerProfile
    """
    if created:
        if instance.role == 'buyer':
            BuyerProfile.objects.create(user=instance)
        elif instance.role == 'dealer':
            DealerProfile.objects.create(user=instance)


@receiver(post_save, sender=CustomUser)
def save_user_profile(sender, instance, **kwargs):
    """
    Save the profile whenever the user object is saved.
    Ensures related profile is updated with user changes if needed.
    """
    if instance.role == 'buyer' and hasattr(instance, 'buyer_profile'):
        instance.buyer_profile.save()
    elif instance.role == 'dealer' and hasattr(instance, 'dealer_profile'):
        instance.dealer_profile.save()
