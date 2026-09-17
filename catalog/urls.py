from django.urls import path

from catalog.views import (
    index,
    ManufacturerListView,
    ManufacturerCreateView,
    ManufacturerUpdateView,
    ManufacturerDeleteView,
    CarListView,
    CarDetailView,
    CarCreateView,
    CarUpdateView,
    CarDeleteView, PartCategoryListView, PartCategoryCreateView, PartCategoryUpdateView, PartCategoryDeleteView,
)

urlpatterns = [
    path("", index, name="index"),
    path(
        "manufacturers/",
        ManufacturerListView.as_view(),
        name="manufacturer-list",
    ),
    path(
        "manufacturers/create/",
        ManufacturerCreateView.as_view(),
        name="manufacturer-create",
    ),
    path(
        "manufacturers/<int:pk>/update/",
        ManufacturerUpdateView.as_view(),
        name="manufacturer-update",
    ),
    path(
        "manufacturers/<int:pk>/delete/",
        ManufacturerDeleteView.as_view(),
        name="manufacturer-delete",
    ),
    path("cars/", CarListView.as_view(), name="car-list"),
    path("cars/<int:pk>/", CarDetailView.as_view(), name="car-detail"),
    path("cars/create/", CarCreateView.as_view(), name="car-create"),
    path("cars/<int:pk>/update/", CarUpdateView.as_view(), name="car-update"),
    path("cars/<int:pk>/delete/", CarDeleteView.as_view(), name="car-delete"),
    path(
        "categories/",
        PartCategoryListView.as_view(),
        name="category-list",
    ),
    path(
        "categories/create/",
        PartCategoryCreateView.as_view(),
        name="category-create",
    ),
    path(
        "categories/<int:pk>/update/",
        PartCategoryUpdateView.as_view(),
        name="category-update",
    ),
    path(
        "categories/<int:pk>/delete/",
        PartCategoryDeleteView.as_view(),
        name="category-delete",
    ),
]

app_name = "catalog"
