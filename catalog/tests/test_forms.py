from django.core.exceptions import ValidationError
from django.test import TestCase

from catalog.forms import (
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
