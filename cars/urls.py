from django.urls import path
from cars.views import HomeView, FavoritesView, toggle_favorite, car_models_by_brand

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path('favorites/', FavoritesView.as_view(), name='favorite-cars'),
    path('ajax/models/<int:brand_id>/', car_models_by_brand, name='ajax_car_models'),
    # path('cars/<slug:slug>/', CarDetailView.as_view(), name='car-detail'),
    path('toggle-favorite/', toggle_favorite, name='toggle_favorite'),
]
