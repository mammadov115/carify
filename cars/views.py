from django.views.generic import ListView
from django.views.generic import DetailView
from cars.models import Car
from django.http import JsonResponse
from django.views.decorators.http import require_POST
# Create your views here.


class HomeView(ListView):
    """
    Displays a list of available cars on the home page.
    """
    model = Car
    template_name = "home.html"
    context_object_name = "cars"
    paginate_by = 2  # Optional: paginate 9 cars per page

    # def get_queryset(self):
    #     """
    #     Return all cars ordered by newest first.
    #     """
    #     return Car.objects.filter(featured=True).order_by('-featured')


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



class CarDetailView(DetailView):
    """
    Displays detailed information for a single car, including its
    images, features, pricing, condition, and customer reviews.
    """
    model = Car
    template_name = "car_detail.html"
    context_object_name = "car"
    slug_field = "slug"
    slug_url_kwarg = "slug"

    def get_queryset(self):
        """
        Optionally filter queryset to include only active or available cars.
        Modify as needed for business logic.
        """
        return Car.objects.all().prefetch_related(
            'features',   # Fetch features to avoid extra queries
            'images',     # Fetch related images efficiently
            'reviews'     # Fetch reviews for display
        )

    def get_context_data(self, **kwargs):
        """
        Adds extra context data for the template.
        """
        context = super().get_context_data(**kwargs)
        context['feature_list'] = self.object.features.all()
        context['image_list'] = self.object.images.all()
        context['reviews'] = self.object.reviews.all()
        return context


class CarListView(ListView):
    """
    Displays a list of all available cars.
    Supports pagination and ordering by newest first.
    """
    model = Car
    template_name = "cars.html"
    context_object_name = "cars"
    paginate_by = 12  # Optional: show 12 cars per page
    ordering = ["-created_at"]

    def get_queryset(self):
        """
        Return all cars ordered by creation date (newest first).
        """
        return Car.objects.all().order_by("-created_at")