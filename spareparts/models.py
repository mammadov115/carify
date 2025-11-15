from django.db import models
from django.utils.text import slugify
from accounts.models import DealerProfile


class SparePartCategory(models.Model):
    """
    Represents a category for spare parts, e.g., Engine, Suspension, Electronics.
    """
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = "Spare Part Category"
        verbose_name_plural = "Spare Part Categories"
        ordering = ['name']

    def __str__(self):
        return self.name


class SparePart(models.Model):
    """
    Represents an individual spare part for cars.
    Includes dealer, category, pricing, availability, images, and description.
    """
    # Dealer
    dealer = models.ForeignKey(
        DealerProfile,
        on_delete=models.SET_NULL,
        null=True,
        related_name='spare_parts'
    )

    # Basic info
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    category = models.ForeignKey(
        SparePartCategory,
        on_delete=models.SET_NULL,
        null=True,
        related_name='spare_parts'
    )

    # Pricing
    price = models.DecimalField(max_digits=10, decimal_places=2)
    is_negotiable = models.BooleanField(default=False)

    # Availability
    in_stock = models.BooleanField(default=True)
    quantity = models.PositiveIntegerField(default=1)

    # Media
    main_image = models.ImageField(upload_to='spare_parts/')
    additional_images = models.ManyToManyField(
        'SparePartImage',
        blank=True,
        related_name='spare_parts'
    )

    # Description
    description = models.TextField(blank=True, null=True)

    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Spare Part"
        verbose_name_plural = "Spare Parts"

    def save(self, *args, **kwargs):
        """
        Automatically generates slug from name if not provided.
        """
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name}"


class SparePartImage(models.Model):
    """
    Represents additional images for a spare part.
    """
    image = models.ImageField(upload_to='spare_parts/gallery/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Image for Spare Part ID {self.id}"
 