from django.core.exceptions import ValidationError
from django.test import TestCase

from catalog.forms import (
    MechanicLicenseUpdateForm,
    validate_license_number,
)


class LicenseValidationTests(TestCase):
    def test_license_number_valid(self):
        valid_license = "MEC12345"
        self.assertEqual(validate_license_number(valid_license), valid_license)

    def test_license_number_invalid_length(self):
        short_license = "MEC123"
        with self.assertRaises(ValidationError):
            validate_license_number(short_license)

        long_license = "MEC1234567"
        with self.assertRaises(ValidationError):
            validate_license_number(long_license)

    def test_license_number_invalid_letters(self):
        with self.assertRaises(ValidationError):
            validate_license_number("mec12345")
        with self.assertRaises(ValidationError):
            validate_license_number("12A12345")

    def test_license_number_invalid_digits(self):
        with self.assertRaises(ValidationError):
            validate_license_number("ABC1234X")
        with self.assertRaises(ValidationError):
            validate_license_number("ABC1234_")


class FormsTests(TestCase):
    def test_mechanic_license_update_form_valid(self):
        form_data = {"license_number": "UKR98765"}
        form = MechanicLicenseUpdateForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_mechanic_license_update_form_invalid(self):
        form_data = {"license_number": "wrong"}
        form = MechanicLicenseUpdateForm(data=form_data)
        self.assertFalse(form.is_valid())
