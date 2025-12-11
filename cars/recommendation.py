from django.db.models import Q, Min, Max
from cars.models import Car
from django.db.models import Q


def recommend_for_car(car_id, limit=6):
    """
    Recommend similar cars based on a single car's attributes.
    Uses brand, model, price, fuel type, year range, engine volume,
    transmission and mileage similarity.
    """
    try:
        car = Car.objects.get(id=car_id)
    except Car.DoesNotExist:
        return Car.objects.none()

    # year_value = car.year.year  # FK → integer
    # engine = float(car.engine_volume)
    
    # Base similarity filters
    queryset = Car.objects.filter(
        # Q(fuel_type=car.fuel_type) &                            # same fuel
        # Q(transmission=car.transmission) &                      # same transmission
        # Q(engine_volume__range=(engine - 0.3, engine + 0.3)) &  # close engine size
        # Q(year__year__range=(year_value - 1, year_value + 1)) & # close years
        Q(total_price__range=(car.total_price - 2000, car.total_price + 2000))     # close price
    ).exclude(id=car.id)

    # Prioritization
    queryset = queryset.order_by(
        'total_price',     # closest price first
        '-brand',          # same brand goes higher
        '-model',          # same model
        'mileage'          # lower mileage is better
    )[:limit]

    return queryset


def recommend_for_general(viewed_ids, limit=10):
    """
    Recommend cars based on multiple user-viewed cars.
    Extracts a viewing profile (brand frequency, fuel, transmission,
    price range, year range, engine volume range, condition)
    and recommends cars matching that profile.
    """

    if not viewed_ids:
        return Car.objects.none()

    viewed = Car.objects.filter(id__in=viewed_ids)

    if not viewed.exists():
        return Car.objects.none()

    # Extract patterns
    brands = viewed.values_list("brand", flat=True)
    models = viewed.values_list("model", flat=True)
    fuels = viewed.values_list("fuel_type", flat=True)
    transmissions = viewed.values_list("transmission", flat=True)
    conditions = viewed.values_list("condition", flat=True)

    # Numeric ranges
    price_min = viewed.aggregate(Min("price"))["price__min"]
    price_max = viewed.aggregate(Max("price"))["price__max"]

    year_min = viewed.aggregate(Min("year__year"))["year__year__min"]
    year_max = viewed.aggregate(Max("year__year"))["year__year__max"]

    engine_min = viewed.aggregate(Min("engine_volume"))["engine_volume__min"]
    engine_max = viewed.aggregate(Max("engine_volume"))["engine_volume__max"]

    mileage_min = viewed.aggregate(Min("mileage"))["mileage__min"]
    mileage_max = viewed.aggregate(Max("mileage"))["mileage__max"]

    queryset = Car.objects.exclude(id__in=viewed_ids)

    # Profile-based filters
    queryset = queryset.filter(
        Q(brand__in=brands) |
        Q(model__in=models) |
        Q(fuel_type__in=fuels) |
        Q(transmission__in=transmissions) |
        Q(condition__in=conditions) |
        Q(price__range=(price_min - 2500, price_max + 2500)) |
        Q(year__year__range=(year_min - 1, year_max + 1)) |
        Q(engine_volume__range=(engine_min - 0.3, engine_max + 0.3)) |
        Q(mileage__range=(mileage_min, mileage_max)) 
    )

    # Prioritization: more relevant cars first
    queryset = queryset.order_by(
        '-brand',
        '-model',
        'price',
        'mileage'
    )[:limit]

    return queryset
