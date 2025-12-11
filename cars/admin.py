from django.contrib import admin
from .models import Car, CarImage, Brand, CarModel, Year
from image_uploader_widget.admin import ImageUploaderInline


class CarImageInline(ImageUploaderInline):
    """
    Inline editor for additional car images.
    """
    model = CarImage
    extra = 0


@admin.register(Car)    
class CarAdmin(admin.ModelAdmin):
    """
    Admin configuration for Car model.
    Includes dealer info, technical specs, pricing, condition, and features.
    """
    list_display = ("brand", "model", "year", "price", "customs_tax_estimate","total_price", "condition")
    list_filter = ("brand", "condition", "fuel_type", "transmission", "is_negotiable")
    search_fields = ("brand", "model")
    inlines = [CarImageInline]
    ordering = ("-created_at",)
    readonly_fields = ("created_at", "updated_at")
    exclude = ("slug",)
    list_editable = ("customs_tax_estimate", )


admin.site.register(Brand)
admin.site.register(CarModel)
admin.site.register(Year)
