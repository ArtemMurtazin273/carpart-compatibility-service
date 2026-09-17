from django.test import TestCase

from catalog.forms import (
    validate_license_number,
)


class LicenseValidationTests(TestCase):
    def test_license_number_valid(self):
        valid_license = "MEC12345"
        self.assertEqual(validate_license_number(valid_license), valid_license)
