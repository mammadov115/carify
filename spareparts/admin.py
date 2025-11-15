from django.contrib import admin
from .models import SparePartCategory, SparePart, SparePartImage


@admin.register(SparePartCategory)
class SparePartCategoryAdmin(admin.ModelAdmin):
    """
    Admin configuration for SparePartCategory.
    Displays name and description, allows search and ordering.
    """
    list_display = ('name', 'description')
    search_fields = ('name',)
    ordering = ('name',)


class SparePartImageInline(admin.TabularInline):
    """
    Inline admin for additional images of SparePart.
    Allows adding multiple images directly in SparePart admin.
    """
    model = SparePart.additional_images.through
    extra = 1


@admin.register(SparePart)
class SparePartAdmin(admin.ModelAdmin):
    """
    Admin configuration for SparePart.
    Displays main fields, allows filtering, searching, and inline additional images.
    """
    list_display = ('name', 'dealer', 'category', 'price', 'is_negotiable', 'in_stock', 'quantity', 'created_at')
    list_filter = ('category', 'dealer', 'in_stock', 'is_negotiable')
    search_fields = ('name', 'description', 'dealer__user__username')
    prepopulated_fields = {'slug': ('name',)}
    inlines = [SparePartImageInline]
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('-created_at',)


@admin.register(SparePartImage)
class SparePartImageAdmin(admin.ModelAdmin):
    """
    Admin configuration for SparePartImage.
    Displays image preview and upload timestamp.
    """
    list_display = ('id', 'image', 'uploaded_at')
    readonly_fields = ('uploaded_at',)
