# cars/signals.py
from django.db.models.signals import pre_delete, pre_save
from django.dispatch import receiver
from .models import Car
# Import CarImage, checking if it exists
try:
    from .models import CarImage
except ImportError:
    # If CarImage does not exist, set it to None, only Car signals will work
    CarImage = None
    
import os
from django.conf import settings

# --- 1. Helper Function to Delete Files ---
def delete_file_if_exists(instance, field_name):
    """
    Checks if a file exists for the given field and deletes it from the filesystem.
    """
    # Get the file object (e.g., instance.main_image)
    file_field = getattr(instance, field_name, None)
    
    # If the file field exists and has a value (path)
    if file_field:
        file_path = file_field.path
        
        # Check if the file actually exists on the disk before attempting deletion
        # This prevents FileNotFoundError if the path is invalid or already deleted
        if os.path.isfile(file_path):
            os.remove(file_path)
            # print(f"INFO: Old file deleted: {file_path}") # For debugging

# --- SIGNALS FOR CAR MODEL (Car.main_image) ---

@receiver(pre_save, sender=Car)
def car_delete_old_main_image_on_update(sender, instance, **kwargs):
    """
    Deletes the old main_image file when the Car object is updated with a new image.
    """
    # Only execute on update (when the primary key (PK) exists)
    if not instance.pk:
        return
    
    # Retrieve the current version of the object from the database
    try:
        old_instance = sender.objects.get(pk=instance.pk)
    except sender.DoesNotExist:
        return

    old_file = old_instance.main_image
    new_file = instance.main_image
    
    # If a new file is uploaded and the old file is different, delete the old one
    if old_file and old_file != new_file:
        delete_file_if_exists(old_instance, 'main_image')


@receiver(pre_delete, sender=Car)
def car_delete_main_image_on_delete(sender, instance, **kwargs):
    """
    Deletes the main_image file from the filesystem when the Car object is deleted.
    """
    delete_file_if_exists(instance, 'main_image')


# --- SIGNALS FOR CARIMAGE MODEL (If it exists) ---

if CarImage:
    @receiver(pre_delete, sender=CarImage)
    def car_image_delete_image_on_delete(sender, instance, **kwargs):
        """
        Deletes the image file (gallery image) when the CarImage object is deleted.
        """
        # Ensure the image field name in CarImage model is 'image'
        delete_file_if_exists(instance, 'image')