from django.urls import path
from .views import CreateOrderView, OrderListView, RemoveOrderItemView, CreateOrderFromProductsView

urlpatterns = [
    path("order/<str:product_type>/<int:product_id>/", CreateOrderView.as_view(), name="create-order"),
    path("orders/", OrderListView.as_view(), name="order-list"),
    path('order/remove/<str:product_type>/<int:product_id>/', RemoveOrderItemView.as_view(), name='order-remove'),
    path("send-orders/", CreateOrderFromProductsView.as_view(), name="send-orders")
]