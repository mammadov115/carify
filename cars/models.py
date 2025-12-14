from django.db import models
from django.utils.text import slugify
from PIL import Image
from django.core.exceptions import ValidationError


class Brand(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class CarModel(models.Model):
    name = models.CharField(max_length=100)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name='models')

    def __str__(self):
        return f"{self.name}"


class Year(models.Model):
    year = models.IntegerField()

    def __str__(self):
        return f"{self.year}"

# Car Features
class CarFeature(models.Model):
    name = models.CharField(
        max_length=100,
        unique=True,
        verbose_name="Feature Name",
        help_text="Example: Automatic Climate Control, Cruise Control"
    )

    def __str__(self):
        return self.name  

#  Pained Parts
class PaintedPart(models.Model):
    car = models.ForeignKey(
        "Car",
        on_delete=models.CASCADE,
        related_name="painted_parts"
    )

    name = models.CharField(
        max_length=100,
        verbose_name="Part Name",
        help_text="Example: Hood, Left Door"
    )

    class Meta:
        verbose_name = "Painted Part"
        verbose_name_plural = "Painted Parts"
        ordering = ("name",)

    def __str__(self):
        return f"{self.car} – {self.name}"

# Changed Parts
class ChangedPart(models.Model):
    car = models.ForeignKey(
        "Car",
        on_delete=models.CASCADE,
        related_name="changed_parts"
    )

    name = models.CharField(
        max_length=100,
        verbose_name="Part Name",
        help_text="Example: Front Bumper, Rear Door"
    )

    class Meta:
        verbose_name = "Changed Part"
        verbose_name_plural = "Changed Parts"
        ordering = ("name",)

    def __str__(self):
        return f"{self.car} – {self.name}"

# Car model
class Car(models.Model):
    """
    Represents a car listing with detailed information,
    including technical specs, pricing, condition,
    main image, and features.
    """


    AUCTION = 'auction'
    KOREA_STOCK = 'korea_stock'
    ON_THE_WAY = 'on_the_way'
    SOLD_OUT = 'sold_out'


    CATEGORY_CHOICES = [
        (AUCTION, 'Hərrac maşınları'),
        (KOREA_STOCK, 'Koreya stokumuz'),
        (ON_THE_WAY, 'Yolda satılır'),
        (SOLD_OUT, 'Satıldı'),

    ]
    
    car_title = models.CharField(
        max_length=120,
        verbose_name="Car Title",
        help_text="Example: Toyota Camry 2020 • Sedan • 2.5L",
        null=True
    )

    vin = models.CharField(
        max_length=17,
        unique=True,
        verbose_name="VIN",
        help_text="17-character Vehicle Identification Number",
        null=True
    )

    features = models.ManyToManyField(
        CarFeature,
        related_name="cars",
        blank=True,
        verbose_name="Features",
    )

    manufacture_date = models.DateField(
        null=True,
        blank=True,
        verbose_name="Manufacture Date",
        help_text="Leave empty if the manufacture date is unknown"
    )

    category = models.CharField(
        max_length=20,
        choices=CATEGORY_CHOICES,
        default=KOREA_STOCK
    )

    featured = models.BooleanField(
        default=False,
        help_text="Check to feature this car on the homepage."
    )
    

    # Basic info
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, null=True)
    model = models.ForeignKey(CarModel, on_delete=models.CASCADE, null=True)
    year = models.ForeignKey(Year, on_delete=models.CASCADE, null=True)
    slug = models.SlugField(max_length=200, unique=True, blank=True)

    # Technical details
    fuel_type = models.CharField(
        max_length=20,
        choices=[
            ('petrol', 'Benzin'),
            ('diesel', 'Dizel'),
            ('hybrid', 'Hibrid'),
            ('electric', 'Elektrik')
        ]
    )

    transmission = models.CharField(
        max_length=20,
        choices=[
            ('automatic', 'Avtomatik'),
            ('manual', 'Mexanika')
        ]
    )

    engine_volume = models.DecimalField(
        max_digits=3,
        decimal_places=1,
        help_text="Example: 1.6, 2.0, 3.5"
    )

    # Pricing
    price = models.DecimalField(max_digits=10, decimal_places=2)
    customs_tax_estimate = models.DecimalField(
        max_digits=10, decimal_places=2,
        null=True,
        help_text="Estimated customs tax for the car."
    )
    total_price = models.DecimalField(
        max_digits=12, 
        decimal_places=2, 
        null=True
    )


    # Condition
    mileage = models.PositiveIntegerField(help_text="km")

    # Media
    main_image = models.ImageField(upload_to='cars/', null=True)
    damage_map = models.ImageField(upload_to='body_maps/', null=True)
    paint_map = models.ImageField(upload_to='body_maps/', null=True)


    # Description
    description = models.TextField(blank=True, null=True)

    # New fields: To store video links
    promotion_video_url = models.CharField(
        max_length=200, 
        blank=True, 
        null=True, 
        help_text="YouTube Link for the car's Promotional Video"
    )
    paint_test_video_url = models.CharField(
        max_length=200, 
        blank=True, 
        null=True, 
        help_text="YouTube Link for the car's Paint Test Video"
    )

    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def save(self, *args, **kwargs):
        """
        Automatically generates slug from brand, model, and year if not provided.
        """
        # First save to get PK
        super().save(*args, **kwargs)

        updated_fields = []

        # Slug generate (only once)
        year = self.manufacture_date.year if self.manufacture_date else None
        new_slug = slugify(f"{self.brand}-{self.model}-{year}-{self.pk}")
        if self.slug != new_slug:
            self.slug = slugify(f"{self.brand}-{self.model}-{year}-{self.pk}")
            updated_fields.append("slug")

        # Total price calculation
        # new_total = (self.price or 0) + (self.customs_tax_estimate or 0)
        # if self.total_price != new_total:
        #     self.total_price = new_total
        #     updated_fields.append("total_price")
        
        # Save only changed fields 
        if updated_fields:
            super().save(update_fields=updated_fields)


        # # Set slug only if blank
        # if not self.slug and self.pk:
        #     super().save(*args, **kwargs)
        #     self.slug = slugify(f"{self.brand}-{self.model}-{self.year}-{self.pk}")
        # super().save(*args, **kwargs)

        # # resize image
        # output_size = (1000, 750)  # fixed container size (width, height)
        # img = Image.open(self.main_image.path)
        # img = img.convert("RGB")  # prevent errors for PNG w/ alpha

        # # resize while keeping aspect ratio (always covers container)
        # img.thumbnail((2000, 1500))  # allow upscaling
        # ratio = max(output_size[0] / img.width, output_size[1] / img.height)
        # new_size = (int(img.width * ratio), int(img.height * ratio))
        # img = img.resize(new_size, Image.LANCZOS)

        # # create background canvas
        # background = Image.new("RGB", output_size, (255, 255, 255))

        # # center position on canvas
        # x = (output_size[0] - new_size[0]) // 2
        # y = (output_size[1] - new_size[1]) // 2
        # background.paste(img, (x, y))

        # # save result
        # background.save(self.main_image.path, quality=90)

        # For body image map


        # Calculate total_price automatically
        # self.total_price = (self.price or 0) + (self.customs_tax_estimate or 0)
        # super().save(*args, **kwargs)

        def resize_image(image_field, output_size=(1000, 750)):
            if not image_field:
                return
            from PIL import Image
            img = Image.open(image_field.path)
            img = img.convert("RGB")
            img.thumbnail((2000, 1500))
            ratio = max(output_size[0] / img.width, output_size[1] / img.height)
            new_size = (int(img.width * ratio), int(img.height * ratio))
            img = img.resize(new_size, Image.LANCZOS)
            background = Image.new("RGB", output_size, (255, 255, 255))
            x = (output_size[0] - new_size[0]) // 2
            y = (output_size[1] - new_size[1]) // 2
            background.paste(img, (x, y))
            background.save(image_field.path, quality=90)

        
        resize_image(self.main_image)
        resize_image(self.damage_map)
        resize_image(self.paint_map)

    def __str__(self):
        return f"{self.brand} {self.model} {self.year}"

# Car images
class CarImage(models.Model):
    """
    Represents additional images for a car.
    Each car can have multiple images in a gallery.
    """
    car = models.ForeignKey(
        Car,
        on_delete=models.CASCADE,
        related_name='images'
    )
    image = models.ImageField(upload_to='cars/gallery/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):

        super().save(*args, **kwargs)

        # resize image
        output_size = (1000, 750)  # fixed container size (width, height)
        img = Image.open(self.image.path)
        img = img.convert("RGB")  # prevent errors for PNG w/ alpha

        # resize while keeping aspect ratio (always covers container)
        img.thumbnail((2000, 1500))  # allow upscaling
        ratio = max(output_size[0] / img.width, output_size[1] / img.height)
        new_size = (int(img.width * ratio), int(img.height * ratio))
        img = img.resize(new_size, Image.LANCZOS)

        # create background canvas
        background = Image.new("RGB", output_size, (255, 255, 255))

        # center position on canvas
        x = (output_size[0] - new_size[0]) // 2
        y = (output_size[1] - new_size[1]) // 2
        background.paste(img, (x, y))

        # save result
        background.save(self.image.path, quality=90)


    def __str__(self):
        return f"Image for {self.car}"
    

# --- 1. Core "About Us" Information (Hero + Mission + CTA) ---

class AboutPage(models.Model):
    """
    Stores the main content for the About Us page, including the Hero section,
    Mission, and Call-to-Action (CTA).
    This model is intended to have only one instance.
    """
    # Hero Section
    hero_title = models.CharField(
        max_length=150, 
        verbose_name="Hero Title",
        default="Korean Quality, On Baku Roads."
    )
    hero_subtitle = models.CharField(
        max_length=255, 
        verbose_name="Hero Subtitle",
        default="Your reliable, transparent, and fast car supply platform."
    )

    # Mission Section
    mission_title = models.CharField(
        max_length=100,
        verbose_name="Mission Title",
        default="Connecting the Markets"
    )
    mission_text_primary = models.TextField(
        verbose_name="Mission Text 1 (Primary)",
        help_text="The first paragraph. Mention the name of the platform."
    )
    mission_text_secondary = models.TextField(
        verbose_name="Mission Text 2 (Secondary)",
        help_text="The second paragraph. Detail the selection and delivery process."
    )
    
    # CTA (Call to Action) Section
    cta_title = models.CharField(
        max_length=100,
        verbose_name="CTA Title",
        default="Start Your Journey with Confidence."
    )
    cta_text = models.CharField(
        max_length=255,
        verbose_name="CTA Text",
        default="Have questions about importing your dream car from Korea? Contact our team."
    )

    class Meta:
        verbose_name = "About Page Core Data"
        verbose_name_plural = "About Page Core Data"

    def __str__(self):
        return "About Page General Information"
    
    # Validation to ensure only one instance of this model can exist
    def clean(self):
        if AboutPage.objects.exists() and not self.pk:
            raise ValidationError('Only one primary "AboutPage" instance can be created.')
        super().clean()


# --- 2. Our Values Section (The differentiating factors) ---

class OurValue(models.Model):
    """
    Stores the key values that differentiate the platform (e.g., Transparency, Quality, Convenience).
    """
    title = models.CharField(max_length=100, verbose_name="Value Title")
    description = models.TextField(max_length=300, verbose_name="Short Description")
    # Field to store the Bootstrap icon class
    icon_name = models.CharField(
        max_length=50, 
        verbose_name="Bootstrap Icon Name",
        help_text="Example: bi-journal-check, bi-tools, bi-truck"
    )
    icon_color = models.CharField(max_length=100, verbose_name="Icon color", help_text="Example: info, danger, sucess")

    order = models.PositiveSmallIntegerField(
        default=0, 
        verbose_name="Display Order", 
        help_text="The order in which the value appears on the page"
    )

    class Meta:
        verbose_name = "Our Value"
        verbose_name_plural = "What Makes Us Different (Values)"
        ordering = ['order']

    def __str__(self):
        return self.title


# --- 3. Work Process Section (How We Work tabs) ---

class WorkProcessStep(models.Model):
    """
    Stores each step in the "How We Work?" section (Car Selection, Logistics, Delivery).
    """
    step_number = models.PositiveSmallIntegerField(
        unique=True, 
        verbose_name="Step Number"
    )
    tab_label = models.CharField(
        max_length=50, 
        verbose_name="Tab Label (Small)",
        help_text="E.g., Selection, Transport, Handover"
    )
    step_title = models.CharField(
        max_length=100, 
        verbose_name="Step Title (Large)"
    )
    step_description = models.TextField(
        verbose_name="Step Description",
        help_text="Detailed text appearing inside the tab."
    )
    # The icon is implicitly handled by the step_number (bi-1-circle, bi-2-circle, etc.)

    class Meta:
        verbose_name = "Work Process Step"
        verbose_name_plural = "Work Process Steps"
        ordering = ['step_number']

    def __str__(self):
        return f"{self.step_number}. {self.tab_label}"
    
