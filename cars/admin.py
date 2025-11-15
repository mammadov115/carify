from django.contrib import admin
from .models import Car, CarFeature, CarImage, CarReview, FavoriteCar
from django import forms
from django.forms.widgets import ClearableFileInput

class CarFeatureInline(admin.TabularInline):
    """
    Inline editor for car features within the Car admin page.
    """
    model = Car.features.through  # ManyToMany through model
    extra = 1


class CarImageInline(admin.TabularInline):
    """
    Inline editor for additional car images.
    """
    model = CarImage
    extra = 1


@admin.register(Car)    
class CarAdmin(admin.ModelAdmin):
    """
    Admin configuration for Car model.
    Includes dealer info, technical specs, pricing, condition, and features.
    """
    list_display = ("brand", "model", "year", "price", "condition", "dealer")
    list_filter = ("brand", "condition", "fuel_type", "transmission", "is_negotiable")
    search_fields = ("brand", "model", "dealer__user__username")
    prepopulated_fields = {"slug": ("brand", "model", "year")}
    inlines = [CarImageInline]
    ordering = ("-created_at",)
    readonly_fields = ("created_at", "updated_at")

    # def save_new_objects(self, formset, commit=True):
    #     # Override to handle multiple uploads
    #     objs = []
    #     for form in formset.forms:
    #         images = form.files.getlist('image')
    #         car = form.instance.car
    #         for img in images:
    #             objs.append(CarImage.objects.create(car=car, image=img))
    #     return objs

@admin.register(CarFeature)
class CarFeatureAdmin(admin.ModelAdmin):
    """
    Admin configuration for CarFeature model.
    """
    list_display = ("name",)
    search_fields = ("name",)
    ordering = ("name",)


@admin.register(CarReview)
class CarReviewAdmin(admin.ModelAdmin):
    """
    Admin configuration for CarReview model.
    """
    list_display = ("car", "user", "rating", "created_at")
    list_filter = ("rating", "created_at")
    search_fields = ("car__brand", "car__model", "user__username")
    readonly_fields = ("created_at",)


@admin.register(FavoriteCar)
class FavoriteCarAdmin(admin.ModelAdmin):
    """
    Admin configuration for FavoriteCar (wishlist) model.
    """
    list_display = ("user", "car", "added_at")
    search_fields = ("user__username", "car__brand", "car__model")
    readonly_fields = ("added_at",)
    list_filter = ("added_at",)
