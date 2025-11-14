from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, BuyerProfile, DealerProfile


class BuyerProfileInline(admin.StackedInline):
    """
    Inline admin for BuyerProfile.
    Shown inside CustomUser admin for buyers.
    """
    model = BuyerProfile
    can_delete = False
    verbose_name_plural = 'Buyer Profile'
    fk_name = 'user'

    def save_model(self, request, obj, form, change):
        obj.clean()
        super().save_model(request, obj, form, change)



class DealerProfileInline(admin.StackedInline):
    """
    Inline admin for DealerProfile.
    Shown inside CustomUser admin for dealers.
    """
    model = DealerProfile
    can_delete = False
    verbose_name_plural = 'Dealer Profile'
    fk_name = 'user'



@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    """
    Admin panel configuration for CustomUser.
    Includes inline BuyerProfile or DealerProfile depending on role.
    """
    inlines = []

    list_display = ('username', 'email', 'first_name', 'last_name', 'role', 'is_staff')
    list_filter = ('role', 'is_staff', 'is_superuser', 'is_active')

    fieldsets = (
        (None, {'fields': ('username', 'email', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name')}),
        ('Permissions', {'fields': ('role', 'is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'role'),
        }),
    )

    search_fields = ('username', 'email', 'first_name', 'last_name')
    ordering = ('username',)

    def get_inline_instances(self, request, obj=None):
        """
        Show inline profile based on the user's role.
        BuyerProfile for buyers, DealerProfile for dealers.
        """
        if not obj:
            return []

        inlines = []
        if obj.role == 'buyer':
            inlines.append(BuyerProfileInline(self.model, self.admin_site))
        elif obj.role == 'dealer':
            inlines.append(DealerProfileInline(self.model, self.admin_site))
        return inlines


@admin.register(BuyerProfile)
class BuyerProfileAdmin(admin.ModelAdmin):
    """
    Admin panel for BuyerProfile.
    Typically shown inline in CustomUserAdmin.
    """
    list_display = ('user','phone_number', 'address')

    def save_model(self, request, obj, form, change):
        obj.clean()
        super().save_model(request, obj, form, change)



@admin.register(DealerProfile)
class DealerProfileAdmin(admin.ModelAdmin):
    """
    Admin panel for DealerProfile.
    Typically shown inline in CustomUserAdmin.
    """
    list_display = ('user', 'company_name', 'tax_number', 'phone_number', 'email', 'address')

    def save_model(self, request, obj, form, change):
        obj.clean()
        super().save_model(request, obj, form, change)
