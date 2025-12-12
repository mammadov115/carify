from django.contrib import admin
from .models import Car, CarImage, Brand, CarModel, Year, AboutPage, OurValue, WorkProcessStep
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
    Includes dealer info, technical specs, pricing, and features.
    """
    list_display = ("brand", "model", "year", "price", "customs_tax_estimate","total_price")
    list_filter = ("brand", "fuel_type", "transmission")
    search_fields = ("brand", "model")
    inlines = [CarImageInline]
    ordering = ("-created_at",)
    readonly_fields = ("created_at", "updated_at")
    exclude = ("slug",)
    list_editable = ("customs_tax_estimate", )


admin.site.register(Brand)
admin.site.register(CarModel)
admin.site.register(Year)


# About Info
# Custom Admin for AboutPage (Enforces Single Instance)

@admin.register(AboutPage)
class AboutPageAdmin(admin.ModelAdmin):
    list_display = ('hero_title', 'cta_title')
    fieldsets = (
        ('Hero Section', {
            'fields': ('hero_title', 'hero_subtitle'),
        }),
        ('Mission Section', {
            'fields': ('mission_title', 'mission_text_primary', 'mission_text_secondary'),
        }),
        ('CTA Section', {
            'fields': ('cta_title', 'cta_text'),
        }),
    )

    # Prevents adding a new instance if one already exists
    def has_add_permission(self, request):
        return not AboutPage.objects.exists()

# Admin for Values
@admin.register(OurValue)
class OurValueAdmin(admin.ModelAdmin):
    list_display = ('title', 'icon_name', 'order')
    list_editable = ('order',)
    search_fields = ('title',)

# Admin for Process Steps
@admin.register(WorkProcessStep)
class WorkProcessStepAdmin(admin.ModelAdmin):
    list_display = ('step_number', 'tab_label', 'step_title')

