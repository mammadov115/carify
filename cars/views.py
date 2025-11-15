from django.views.generic import ListView
# from django.contrib.auth.mixins import LoginRequiredMixin
from cars.models import Car
# Create your views here.


class HomeView(ListView):
    """
    Displays a list of available cars on the home page.
    Only authenticated users can access this view.
    """
    model = Car
    template_name = "home.html"
    context_object_name = "cars"
    login_url = "login"
    paginate_by = 9  # Optional: paginate 9 cars per page

    def get_queryset(self):
        """
        Return all cars ordered by newest first.
        """
        return Car.objects.all().order_by('-created_at')