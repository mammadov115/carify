from django.urls import path
from cars.views import HomeView, FavoritesView, CarDetailView, toggle_favorite, car_models_by_brand, AboutUsView

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path('favorites/', FavoritesView.as_view(), name='favorite-cars'),
    path('ajax/models/<int:brand_id>/', car_models_by_brand, name='ajax_car_models'),
    path("car/<slug:slug>/", CarDetailView.as_view(), name="car_detail"),
    path('toggle-favorite/', toggle_favorite, name='toggle_favorite'),
    path("about-us/", AboutUsView.as_view(), name="about_us"),

]
