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
    CarDeleteView,
    PartCategoryListView,
    PartCategoryCreateView,
    PartCategoryUpdateView,
    PartCategoryDeleteView,
    PartListView,
    PartDetailView,
    PartCreateView,
    PartUpdateView,
    PartDeleteView,
    toggle_assign_to_part,
    MechanicListView,
    MechanicDetailView,
    MechanicCreateView,
    MechanicLicenseUpdateView,
    MechanicDeleteView, SignUpView,
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
    path("parts/", PartListView.as_view(), name="part-list"),
    path("parts/<int:pk>/", PartDetailView.as_view(), name="part-detail"),
    path("parts/create/", PartCreateView.as_view(), name="part-create"),
    path("parts/<int:pk>/update/", PartUpdateView.as_view(), name="part-update"),
    path("parts/<int:pk>/delete/", PartDeleteView.as_view(), name="part-delete"),
    path(
        "parts/<int:pk>/toggle-assign/",
        toggle_assign_to_part,
        name="toggle-part-assign",
    ),
    path("mechanics/", MechanicListView.as_view(), name="mechanic-list"),
    path(
        "mechanics/<int:pk>/",
        MechanicDetailView.as_view(),
        name="mechanic-detail",
    ),
    path("mechanics/create/", MechanicCreateView.as_view(), name="mechanic-create"),
    path(
        "mechanics/<int:pk>/update/",
        MechanicLicenseUpdateView.as_view(),
        name="mechanic-update",
    ),
    path(
        "mechanics/<int:pk>/delete/",
        MechanicDeleteView.as_view(),
        name="mechanic-delete",
    ),
    path("register/", SignUpView.as_view(), name="register"),
]

app_name = "catalog"
