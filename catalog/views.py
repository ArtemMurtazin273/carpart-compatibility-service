from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views import generic

from catalog.forms import ManufacturerSearchForm, CarSearchForm, CategorySearchForm, PartSearchForm, PartForm, \
    MechanicSearchForm, MechanicCreationForm, MechanicLicenseUpdateForm
from catalog.models import Car, Manufacturer, Part, PartCategory, Mechanic


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


class CarDetailView(LoginRequiredMixin, generic.DetailView):
    model = Car
    queryset = Car.objects.prefetch_related("parts__manufacturer")


class CarCreateView(LoginRequiredMixin, generic.CreateView):
    model = Car
    fields = "__all__"
    success_url = reverse_lazy("catalog:car-list")


class CarUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Car
    fields = "__all__"
    success_url = reverse_lazy("catalog:car-list")


class CarDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Car
    success_url = reverse_lazy("catalog:car-list")


class PartCategoryListView(LoginRequiredMixin, generic.ListView):
    model = PartCategory
    paginate_by = 5
    template_name = "catalog/category_list.html"
    context_object_name = "category_list"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        name = self.request.GET.get("name", "")
        context["search_form"] = CategorySearchForm(
            initial={"name": name}
        )
        return context

    def get_queryset(self):
        queryset = PartCategory.objects.all()
        form = CategorySearchForm(self.request.GET)
        if form.is_valid():
            return queryset.filter(name__icontains=form.cleaned_data["name"])
        return queryset


class PartCategoryCreateView(LoginRequiredMixin, generic.CreateView):
    model = PartCategory
    fields = "__all__"
    template_name = "catalog/category_form.html"
    success_url = reverse_lazy("catalog:category-list")


class PartCategoryUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = PartCategory
    fields = "__all__"
    template_name = "catalog/category_form.html"
    success_url = reverse_lazy("catalog:category-list")


class PartCategoryDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = PartCategory
    template_name = "catalog/category_confirm_delete.html"
    success_url = reverse_lazy("catalog:category-list")


class PartListView(LoginRequiredMixin, generic.ListView):
    model = Part
    paginate_by = 5

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        name = self.request.GET.get("name", "")
        context["search_form"] = PartSearchForm(
            initial={"name": name}
        )
        return context

    def get_queryset(self):
        queryset = Part.objects.select_related("manufacturer", "category")
        form = PartSearchForm(self.request.GET)
        if form.is_valid():
            return queryset.filter(name__icontains=form.cleaned_data["name"])
        return queryset


class PartDetailView(LoginRequiredMixin, generic.DetailView):
    model = Part
    queryset = Part.objects.select_related("manufacturer", "category").prefetch_related(
        "cars", "mechanics"
    )


class PartCreateView(LoginRequiredMixin, generic.CreateView):
    model = Part
    form_class = PartForm
    success_url = reverse_lazy("catalog:part-list")


class PartUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Part
    form_class = PartForm
    success_url = reverse_lazy("catalog:part-list")


class PartDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Part
    success_url = reverse_lazy("catalog:part-list")


@login_required
def toggle_assign_to_part(request, pk):
    part = get_object_or_404(Part, pk=pk)
    mechanic = request.user
    if mechanic in part.mechanics.all():
        part.mechanics.remove(mechanic)
    else:
        part.mechanics.add(mechanic)
    return HttpResponseRedirect(reverse_lazy("catalog:part-detail", args=[pk]))


class MechanicListView(LoginRequiredMixin, generic.ListView):
    model = Mechanic
    paginate_by = 5

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        username = self.request.GET.get("username", "")
        context["search_form"] = MechanicSearchForm(
            initial={"username": username}
        )
        return context

    def get_queryset(self):
        queryset = Mechanic.objects.all()
        form = MechanicSearchForm(self.request.GET)
        if form.is_valid():
            return queryset.filter(
                username__icontains=form.cleaned_data["username"]
            )
        return queryset


class MechanicDetailView(LoginRequiredMixin, generic.DetailView):
    model = Mechanic
    queryset = Mechanic.objects.prefetch_related("parts__manufacturer")


class MechanicCreateView(LoginRequiredMixin, generic.CreateView):
    model = Mechanic
    form_class = MechanicCreationForm
    success_url = reverse_lazy("catalog:mechanic-list")


class MechanicLicenseUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Mechanic
    form_class = MechanicLicenseUpdateForm
    success_url = reverse_lazy("catalog:mechanic-list")
