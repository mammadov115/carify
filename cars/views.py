from django.views.generic import ListView
from django.views.generic import DetailView
from cars.models import Car, Brand, CarModel, Year
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.db.models import Case, When
from django.db.models import Q
# Create your views here.


class HomeView(ListView):
    """
    Displays a list of available cars on the home page with filtering.
    """
    model = Car
    template_name = "home.html"
    context_object_name = "cars"
    paginate_by = 11
    ordering = ["-created_at"]

    def get_queryset(self):
        qs = super().get_queryset()

        # Filter based on GET parameters
        category = self.request.GET.get("category")
        brand_id = self.request.GET.get("brand")
        model_id = self.request.GET.get("model")
        year_id = self.request.GET.get("year")

        filters = Q()
        if category:
            filters &= Q(category=category)
        if brand_id:
            filters &= Q(brand_id=brand_id)
        if model_id:
            filters &= Q(model_id=model_id)
        if year_id:
            filters &= Q(year_id=year_id)

        return qs.filter(filters)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['brands'] = Brand.objects.all()
        context['car_models'] = CarModel.objects.all()
        context['years'] = Year.objects.all()

        # Track selected filters for template
        context['selected_category'] = self.request.GET.get("category", "")
        context['selected_brand'] = int(self.request.GET.get("brand")) if self.request.GET.get("brand") else None
        context['selected_model'] = int(self.request.GET.get("model")) if self.request.GET.get("model") else None
        context['selected_year'] = int(self.request.GET.get("year")) if self.request.GET.get("year") else None

        return context

@require_POST
def toggle_favorite(request):
    car_id = request.POST.get('car_id')
    if not car_id:
        return JsonResponse({"success": False, "error": "No car id provided."})

    # initialize session list if it doesn't exist
    favorites = request.session.get('favorites', [])

    if car_id in favorites:
        favorites.remove(car_id)
        added = False
    else:
        favorites.append(car_id)
        added = True

    request.session['favorites'] = favorites
    request.session.modified = True

    return JsonResponse({"success": True, "added": added, "favorites_count": len(favorites)})

def car_models_by_brand(request, brand_id):
    models = CarModel.objects.filter(brand_id=brand_id).values('id', 'name')
    print(brand_id)
    return JsonResponse(list(models), safe=False)


# class CarDetailView(DetailView):
#     """
#     Displays detailed information for a single car, including its
#     images, features, pricing, condition, and customer reviews.
#     """
#     model = Car
#     template_name = "car_detail.html"
#     context_object_name = "car"
#     slug_field = "slug"
#     slug_url_kwarg = "slug"

#     def get_queryset(self):
#         """
#         Optionally filter queryset to include only active or available cars.
#         Modify as needed for business logic.
#         """
#         return Car.objects.all().prefetch_related(
#             'features',   # Fetch features to avoid extra queries
#             'images',     # Fetch related images efficiently
#             'reviews'     # Fetch reviews for display
#         )

#     def get_context_data(self, **kwargs):
#         """
#         Adds extra context data for the template.
#         """
#         context = super().get_context_data(**kwargs)
#         context['feature_list'] = self.object.features.all()
#         context['image_list'] = self.object.images.all()
#         context['reviews'] = self.object.reviews.all()
#         return context


class FavoritesView(ListView):
    """
    Displays a list of all favorite cars.
    Supports pagination and ordering by newest first.
    """
    model = Car
    template_name = "favorites.html"
    context_object_name = "cars"
    paginate_by = 12  # Optional: show 12 cars per page

    def get_queryset(self):
        # Get list of favorite car IDs from session
        favorite_ids = self.request.session.get('favorites', [])

        # If no favorites, return empty queryset
        if not favorite_ids:
            return Car.objects.none()

        # Fetch only cars in favorites list
        # Case/When preserves the list order stored in session
        order = Case(*[
            When(id=cid, then=pos) for pos, cid in enumerate(reversed(favorite_ids))
        ])

        print(order)

        return Car.objects.filter(id__in=favorite_ids).order_by(order)
