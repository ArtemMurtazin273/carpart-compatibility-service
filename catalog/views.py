from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from catalog.models import Car, Manufacturer, Part, PartCategory


@login_required
def index(request):
    num_parts = Part.objects.count()
    num_cars = Car.objects.count()
    num_manufacturers = Manufacturer.objects.count()
    num_mechanics = get_user_model().objects.count()
    num_categories = PartCategory.objects.count()

    num_visits = request.session.get("num_visits", 0)
    request.session["num_visits"] = num_visits + 1

    context = {
        "num_parts": num_parts,
        "num_cars": num_cars,
        "num_manufacturers": num_manufacturers,
        "num_mechanics": num_mechanics,
        "num_categories": num_categories,
        "num_visits": num_visits + 1,
    }

    return render(request, "catalog/index.html", context=context)
