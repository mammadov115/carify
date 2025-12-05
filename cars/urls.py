from django.urls import path
from cars.views import HomeView, FavoritesView, toggle_favorite

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path('favorites/', FavoritesView.as_view(), name='favorite-cars'),
    # path('cars/<slug:slug>/', CarDetailView.as_view(), name='car-detail'),
    path('toggle-favorite/', toggle_favorite, name='toggle_favorite'),
]
