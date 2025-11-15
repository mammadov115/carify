from django.contrib import admin
from django.contrib.contenttypes.admin import GenericTabularInline, GenericStackedInline
from .models import Order


class OrderInline(GenericTabularInline):
    """
    Inline view for orders in related models (Car or SparePart).
    """
    model = Order
    extra = 1
    readonly_fields = ('created_at', 'updated_at')


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    """
    Admin configuration for the Order model.
    Displays user, ordered item, quantity, and status.
    """
    list_display = ('id', 'user', 'item', 'quantity', 'is_confirmed', 'created_at')
    list_filter = ('is_confirmed', 'created_at', 'content_type')
    search_fields = ('user__username', 'item__name')
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('-created_at',)
