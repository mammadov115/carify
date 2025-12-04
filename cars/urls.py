from django.urls import path
from cars.views import HomeView, CarDetailView, CarListView, toggle_favorite

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path('cars/', CarListView.as_view(), name='cars'),
    path('cars/<slug:slug>/', CarDetailView.as_view(), name='car-detail'),
    path('toggle-favorite/', toggle_favorite, name='toggle_favorite'),
]
