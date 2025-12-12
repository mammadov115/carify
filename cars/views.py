from django.views.generic import ListView, DetailView, TemplateView
from cars.models import Car, Brand, CarModel, Year, AboutPage, OurValue, WorkProcessStep
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.db.models import Case, When
from django.db.models import Q, Min, Max
from django.shortcuts import get_object_or_404
from .recommendation import recommend_for_car

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
        from_year = self.request.GET.get("from_year")  # from slider value
        to_year = self.request.GET.get("to_year")      # to slider value

        filters = Q()
        if category:
            filters &= Q(category=category)
        if brand_id:
            filters &= Q(brand_id=brand_id)
        if model_id:
            filters &= Q(model_id=model_id)
        # Filter by year range from sliders
        if from_year:
            filters &= Q(year__year__gte=int(from_year))  # greater or equal to from_year
        if to_year:
            filters &= Q(year__year__lte=int(to_year))    # less or equal to to_year

        return qs.filter(filters)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['brands'] = Brand.objects.all()
        context['car_models'] = CarModel.objects.all()

        # Adding min and max date
        year_stats = Year.objects.aggregate(min_year=Min('year'), max_year=Max('year'))
        context['min_year'] = year_stats['min_year']
        context['max_year'] = year_stats['max_year']

        # Track selected filters for template
        context['selected_category'] = self.request.GET.get("category", "")
        context['selected_brand'] = int(self.request.GET.get("brand")) if self.request.GET.get("brand") else None
        context['selected_model'] = int(self.request.GET.get("model")) if self.request.GET.get("model") else None
        # Track selected slider values for template
        context['selected_from_year'] = int(self.request.GET.get("from_year")) if self.request.GET.get("from_year") else context['min_year']
        context['selected_to_year'] = int(self.request.GET.get("to_year")) if self.request.GET.get("to_year") else context['max_year']

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

class CarDetailView(DetailView):
    """
    Displays a detailed page for a single car listing.
    Fetches the car object by its slug for SEO-friendly URLs.
    """
    model = Car
    template_name = "car_detail.html"  # Update to your template path
    context_object_name = "car"  # Optional: easier access in template

    def get_object(self, queryset=None):
        """
        Override the default lookup to fetch the car by slug.
        Ensures a 404 page instead of crashing if slug is invalid.
        """
        slug = self.kwargs.get("slug")
        return get_object_or_404(Car, slug=slug)

    def get_context_data(self, **kwargs):
        """
        Add any extra data you want to show in the template.
        Example: features, recommended cars, etc.
        """
        context = super().get_context_data(**kwargs)

        # Get the current Car object fetched by DetailView
        car_object = self.object 
        
        # ----------------------------------------------------------------------
        # Retrieve the 17th image object (index 16) from the images queryset
        # ----------------------------------------------------------------------
        
        try:
            # Queryset slicing: car_object.images.all()[16] directly fetches the 17th item.
            # Using slicing on a QuerySet is efficient as Django handles the limit in SQL.
            seventeenth_image = car_object.images.all()[16] 
        except IndexError:
            # Handle the case where the car has less than 17 images.
            # Set it to None or the last available image if needed.
            seventeenth_image = None
        except AttributeError:
            # Handle if the 'images' attribute doesn't exist or is invalid.
            seventeenth_image = None

        # Add the retrieved object to the context
        context["seventeenth_image"] = seventeenth_image
        
        # -----------------------------
        # Recommended cars for this car
        # -----------------------------
        recommended_cars = recommend_for_car(car_object.id, limit=6)
        context["recommended_cars"] = recommended_cars
        return context


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

        return Car.objects.filter(id__in=favorite_ids).order_by(order)


class AboutUsView(TemplateView):
    """
    Class-Based View for the 'About Us' page.
    It fetches all dynamic content (AboutPage, OurValue, WorkProcessStep)
    and passes it to the template.
    """
    template_name = 'about.html'  # Define the template name

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # 1. Core Page Data (Should only be one object)
        # Safely attempt to get the single AboutPage object
        about_page_data = AboutPage.objects.first()

        # 2. Values Section (Ordered by the 'order' field)
        values = OurValue.objects.all().order_by('order')

        # 3. Work Process Steps (Ordered by the 'step_number' field)
        process_steps = WorkProcessStep.objects.all().order_by('step_number')

        # Add data to the context
        context['about_page_data'] = about_page_data
        context['values'] = values
        context['process_steps'] = process_steps
        
        return context