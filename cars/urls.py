from django.urls import path
from .views import HomeView
from .views import CarDetailView, CarListView

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path('cars/', CarListView.as_view(), name='cars'),
    path('cars/<slug:slug>/', CarDetailView.as_view(), name='car-detail'),
]
