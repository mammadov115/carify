from django.db import models
from cars.models import Car
from spareparts.models import SparePart
from accounts.models import CustomUser


class Order(models.Model):
    """
    Represents a single order by a user.
    An order can have multiple items (cars or spare parts).
    """
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='orders')
    buyer_number = models.CharField(max_length=20)  # phone number or contact
    notes = models.TextField(blank=True, null=True)
    is_confirmed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Order #{self.id} by {self.user}"


class OrderItem(models.Model):
    """
    Represents a single product in an order.
    Can be either a Car or a SparePart.
    """
    ORDER_PRODUCT_TYPE = (
        ('car', 'Car'),
        ('sparepart', 'SparePart'),
    )

    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product_type = models.CharField(max_length=20, choices=ORDER_PRODUCT_TYPE)
    car = models.ForeignKey(Car, null=True, blank=True, on_delete=models.SET_NULL)
    spare_part = models.ForeignKey(SparePart, null=True, blank=True, on_delete=models.SET_NULL)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return f"{self.product_type.title()} in Order #{self.order.id}"

    @property
    def product(self):
        """Returns the actual product object"""
        return self.car if self.product_type == 'car' else self.spare_part
