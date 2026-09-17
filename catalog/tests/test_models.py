from django.contrib.auth import get_user_model
from django.test import TestCase

from catalog.models import Car, Manufacturer, Part, PartCategory


class ModelsTests(TestCase):
    def test_mechanic_str(self):
        mechanic = get_user_model().objects.create_user(
            username="johndoe",
            password="secretpassword123",
            first_name="John",
            last_name="Doe",
            license_number="MEC12345",
        )
        self.assertEqual(
            str(mechanic),
            f"{mechanic.username} ({mechanic.first_name} {mechanic.last_name})"
        )
