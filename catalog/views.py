from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic

from catalog.forms import ManufacturerSearchForm, CarSearchForm
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


class ManufacturerListView(LoginRequiredMixin, generic.ListView):
    model = Manufacturer
    paginate_by = 5

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        name = self.request.GET.get("name", "")
        context["search_form"] = ManufacturerSearchForm(
            initial={"name": name}
        )
        return context

    def get_queryset(self):
        queryset = Manufacturer.objects.all()
        form = ManufacturerSearchForm(self.request.GET)
        if form.is_valid():
            return queryset.filter(name__icontains=form.cleaned_data["name"])
        return queryset


class ManufacturerCreateView(LoginRequiredMixin, generic.CreateView):
    model = Manufacturer
    fields = "__all__"
    success_url = reverse_lazy("catalog:manufacturer-list")


class ManufacturerUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Manufacturer
    fields = "__all__"
    success_url = reverse_lazy("catalog:manufacturer-list")


class ManufacturerDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Manufacturer
    success_url = reverse_lazy("catalog:manufacturer-list")


class CarListView(LoginRequiredMixin, generic.ListView):
    model = Car
    paginate_by = 5

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        model = self.request.GET.get("model", "")
        context["search_form"] = CarSearchForm(
            initial={"model": model}
        )
        return context

    def get_queryset(self):
        queryset = Car.objects.all()
        form = CarSearchForm(self.request.GET)
        if form.is_valid():
            return queryset.filter(model__icontains=form.cleaned_data["model"])
        return queryset
