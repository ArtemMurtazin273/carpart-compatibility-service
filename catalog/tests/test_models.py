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

    def test_manufacturer_str(self):
        manufacturer = Manufacturer.objects.create(
            name="Bosch",
            country="Germany",
        )
        self.assertEqual(str(manufacturer), "Bosch (Germany)")

    def test_category_str(self):
        category = PartCategory.objects.create(
            name="Braking System",
            description="Brake pads, rotors, and calipers",
        )
        self.assertEqual(str(category), "Braking System")

    def test_car_str(self):
        car = Car.objects.create(
            make="Volkswagen",
            model="Golf",
            year=2012,
        )
        self.assertEqual(str(car), "Volkswagen Golf (2012)")
