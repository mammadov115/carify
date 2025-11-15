from django.db import models
from accounts.models import CustomUser



class Order(models.Model):
    """
    Represents an order for a product, which can be either a Car or a SparePart.
    The actual product instance can be accessed via the `product` property.
    """
    PRODUCT_CHOICES = (
        ('car', 'Car'),
        ('sparepart', 'SparePart'),
    )

    # User who made the order
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='orders'
    )

    # Product information
    product_type = models.CharField(
        max_length=20,
        choices=PRODUCT_CHOICES,
        help_text="Select whether the order is for a Car or a SparePart."
    )
    product_id = models.PositiveIntegerField(
        help_text="ID of the selected product."
    )

    # Order details
    quantity = models.PositiveIntegerField(
        default=1,
        help_text="Number of units ordered."
    )
    is_confirmed = models.BooleanField(
        default=False,
        help_text="Whether the order has been confirmed."
    )

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Order"
        verbose_name_plural = "Orders"

    @property
    def product(self):
        """
        Returns the actual product instance based on the product_type and product_id.
        If the product does not exist, returns None.
        """
        if self.product_type == 'car':
            from cars.models import Car
            return Car.objects.filter(id=self.product_id).first()
        elif self.product_type == 'sparepart':
            from spareparts.models import SparePart
            return SparePart.objects.filter(id=self.product_id).first()
        return None

    def __str__(self):
        product_instance = self.product
        product_name = product_instance.name if product_instance else "Unknown Product"
        return f"Order #{self.id} by {self.user} for {product_name}"
