from django.urls import path

from .views import index, OrderListView, OrderCreateView, OrderUpdateView, OrderDetailView, OrderDeleteView, \
    ClientListView, ClientDetailView, ClientDeleteView, ClientCreateView, ClientUpdateView, WorkerListView, \
    WorkerDetailView, WorkerCreateView, WorkerUpdateView, ServiceCategoryListView, ServiceCategoryDeleteView, \
    ServiceCategoryCreateView

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
    path("clients/", ClientListView.as_view(), name="client-list"),
    path("clients/<int:pk>/", ClientDetailView.as_view(), name="client-detail"),
    path("clients/<int:pk>/delete/", ClientDeleteView.as_view(), name="client-delete"),
    path("clients/create/", ClientCreateView.as_view(), name="client-create"),
    path(
        "clients/<int:pk>/update/",
        ClientUpdateView.as_view(),
        name="client-update",
    ),
    path("workers/", WorkerListView.as_view(), name="worker-list"),
    path("workers/<int:pk>/", WorkerDetailView.as_view(), name="worker-detail"),
    path("workers/create/", WorkerCreateView.as_view(), name="worker-create"),
    path(
        "workers/<int:pk>/update/",
        WorkerUpdateView.as_view(),
        name="worker-update",
    ),
    path(
        "servicecategory/",
        ServiceCategoryListView.as_view(),
        name="service-category-list",
    ),
    path(
        "servicecategory/<int:pk>/delete/",
        ServiceCategoryDeleteView.as_view(),
        name="service-category-delete",
    ),

    path(
        "servicecategory/create/",
        ServiceCategoryCreateView.as_view(),
        name="service-category-create",
    ),
]
