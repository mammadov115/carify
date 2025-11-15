from django.contrib import admin
from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    """
    Inline admin for displaying OrderItem objects inside the Order admin page.
    Allows adding/editing multiple items per order.
    """
    model = OrderItem
    extra = 1
    readonly_fields = ('product',)
    fields = ('product_type', 'car', 'spare_part', 'quantity', 'price', 'product')
    autocomplete_fields = ('car', 'spare_part')


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    """
    Admin configuration for the Order model.
    Displays buyer info, notes, and inline order items.
    """
    list_display = ('id', 'user', 'buyer_number', 'is_confirmed', 'created_at', 'updated_at')
    list_filter = ('is_confirmed', 'created_at', 'updated_at')
    search_fields = ('user__username', 'buyer_number', 'notes')
    readonly_fields = ('created_at', 'updated_at')
    inlines = [OrderItemInline]
    ordering = ('-created_at',)
    fieldsets = (
        (None, {
            'fields': ('user', 'buyer_number', 'notes', 'is_confirmed')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at')
        }),
    )


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    """
    Admin configuration for the OrderItem model.
    Allows quick filtering and searching by product type.
    """
    list_display = ('id', 'order', 'product_type', 'product', 'quantity', 'price')
    list_filter = ('product_type',)
    search_fields = ('order__id', 'car__name', 'spare_part__name')
    autocomplete_fields = ('car', 'spare_part')
