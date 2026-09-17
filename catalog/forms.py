from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

from catalog.models import Mechanic, Car, Part


def validate_license_number(license_number):
    if len(license_number) != 8:
        raise ValidationError("License number must consist of exactly 8 characters.")
    if not license_number[:3].isupper() or not license_number[:3].isalpha():
        raise ValidationError("First 3 characters must be uppercase letters.")
    if not license_number[3:].isdigit():
        raise ValidationError("Last 5 characters must be digits.")
    return license_number


class MechanicCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Mechanic
        fields = UserCreationForm.Meta.fields + (
            "license_number",
            "first_name",
            "last_name",
            "email",
        )

    def clean_license_number(self):
        return validate_license_number(self.cleaned_data["license_number"])


class MechanicLicenseUpdateForm(forms.ModelForm):
    class Meta:
        model = Mechanic
        fields = ("license_number",)

    def clean_license_number(self):
        return validate_license_number(self.cleaned_data["license_number"])


class PartForm(forms.ModelForm):
    cars = forms.ModelMultipleChoiceField(
        queryset=Car.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )

    class Meta:
        model = Part
        fields = "__all__"


class CarSearchForm(forms.Form):
    model = forms.CharField(
        max_length=255,
        required=False,
        label="",
        widget=forms.TextInput(attrs={"placeholder": "Search by model"}),
    )


class PartSearchForm(forms.Form):
    name = forms.CharField(
        max_length=255,
        required=False,
        label="",
        widget=forms.TextInput(attrs={"placeholder": "Search by part name"}),
    )


class ManufacturerSearchForm(forms.Form):
    name = forms.CharField(
        max_length=255,
        required=False,
        label="",
        widget=forms.TextInput(attrs={"placeholder": "Search by name"}),
    )


class MechanicSearchForm(forms.Form):
    username = forms.CharField(
        max_length=255,
        required=False,
        label="",
        widget=forms.TextInput(attrs={"placeholder": "Search by username"}),
    )


class CategorySearchForm(forms.Form):
    name = forms.CharField(
        max_length=255,
        required=False,
        label="",
        widget=forms.TextInput(attrs={"placeholder": "Search by category name"}),
    )
