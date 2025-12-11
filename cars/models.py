from django.db import models
from django.utils.text import slugify
from PIL import Image


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
    

    category = models.CharField(
        max_length=20,
        choices=CATEGORY_CHOICES,
        default=KOREA_STOCK
    )

    changed_parts_count = models.PositiveIntegerField(
        default=0,
        help_text="Number of parts replaced on the vehicle"
    )

    painted_parts_count = models.PositiveIntegerField(
        default=0,
        help_text="Number of body parts that have been repainted"
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
        help_text="Estimated customs tax for the car (in USD)."
    )
    total_price = models.DecimalField(
        max_digits=12, 
        decimal_places=2, 
        null=True
    )

    is_negotiable = models.BooleanField(default=False)

    # Condition
    condition = models.CharField(
        max_length=20,
        choices=[
            ('new', 'New'),
            ('used', 'Used')
        ]
    )
    mileage = models.PositiveIntegerField(help_text="km")

    # Media
    main_image = models.ImageField(upload_to='cars/', null=True)

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
        if not self.slug:
            super().save(*args, **kwargs)
            self.slug = slugify(f"{self.brand}-{self.model}-{self.year}-{self.pk}")
        super().save(*args, **kwargs)

        # resize image
        output_size = (1000, 750)  # fixed container size (width, height)
        img = Image.open(self.main_image.path)
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
        background.save(self.main_image.path, quality=90)

        # Calculate total_price automatically
        self.total_price = (self.price or 0) + (self.customs_tax_estimate or 0)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.brand} {self.model} {self.year}"


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