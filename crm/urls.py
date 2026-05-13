from django.urls import path

from .views import index, OrderListView, OrderCreateView

app_name = "crm"

urlpatterns = [
    path("", index, name="index"),
    path(
        "orders/",
        OrderListView.as_view(),
        name="order-list",
    ),
    path("orders/create/", OrderCreateView.as_view(), name="order-create"),
]
