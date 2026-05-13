from django.urls import path

from .views import index, OrderListView, OrderCreateView, OrderUpdateView, OrderDetailView, OrderDeleteView

app_name = "crm"

urlpatterns = [
    path("", index, name="index"),
    path(
        "orders/",
        OrderListView.as_view(),
        name="order-list",
    ),
    path("orders/create/", OrderCreateView.as_view(), name="order-create"),
path(
        "orders/<int:pk>/update/",
        OrderUpdateView.as_view(),
        name="order-update",
    ),
path(
        "orders/<int:pk>/",
        OrderDetailView.as_view(),
        name="order-detail",
    ),
    path(
        "orders/<int:pk>/delete/",
        OrderDeleteView.as_view(),
        name="order-delete",
    ),
]
