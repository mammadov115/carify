import random
from cars.models import Car, Brand, CarModel, Year

# Brands və CarModels
brands = [
    Brand.objects.get_or_create(name="Toyota")[0],
    Brand.objects.get_or_create(name="Hyundai")[0],
    Brand.objects.get_or_create(name="Kia")[0],
]

car_models = {
    "Toyota": ["Corolla", "Camry", "RAV4"],
    "Hyundai": ["Elantra", "Sonata", "Tucson"],
    "Kia": ["Sportage", "Rio", "Sorento"]
}

years = [Year.objects.get_or_create(year=y)[0] for y in range(2018, 2024)]

categories = [Car.AUCTION, Car.KOREA_STOCK, Car.ON_THE_WAY]
fuel_types = ["petrol", "diesel", "hybrid", "electric"]
transmissions = ["automatic", "manual"]
conditions = ["new", "used"]

# 20 fake car
for i in range(1, 21):
    brand = random.choice(brands)
    model_name = random.choice(car_models[brand.name])
    model = CarModel.objects.get_or_create(name=model_name, brand=brand)[0]
    year = random.choice(years)

    slug = f"{brand.name.lower()}-{model.name.lower()}-{year.year}-{i}"

    Car.objects.create(
        category=random.choice(categories),
        featured=random.choice([True, False]),
        brand=brand,
        model=model,
        year=year,
        slug=slug,
        fuel_type=random.choice(fuel_types),
        transmission=random.choice(transmissions),
        engine_volume=round(random.uniform(1.2, 3.5), 1),
        price=round(random.uniform(10000, 50000), 2),
        is_negotiable=random.choice([True, False]),
        condition=random.choice(conditions),
        mileage=random.randint(0, 120000),
        description=f"Fake car {brand.name} {model.name} {year.year}, sample listing."
    )

print("20 fake cars created successfully! 🚗")
