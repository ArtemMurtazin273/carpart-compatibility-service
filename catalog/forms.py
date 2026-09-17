from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

from catalog.models import Mechanic


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
