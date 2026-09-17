from decimal import Decimal

from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from catalog.models import Car, Manufacturer, Part, PartCategory

INDEX_URL = reverse("catalog:index")
PARTS_URL = reverse("catalog:part-list")
CARS_URL = reverse("catalog:car-list")


class PublicViewsTests(TestCase):
    def setUp(self):
        self.client = Client()

    def test_login_required_for_index(self):
        response = self.client.get(INDEX_URL)
        self.assertNotEqual(response.status_code, 200)
        self.assertRedirects(response, f"/accounts/login/?next={INDEX_URL}")

    def test_login_required_for_parts_list(self):
        response = self.client.get(PARTS_URL)
        self.assertNotEqual(response.status_code, 200)
        self.assertRedirects(response, f"/accounts/login/?next={PARTS_URL}")


class PrivateDashboardTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = get_user_model().objects.create_user(
            username="mechanic1",
            password="securepassword123",
            license_number="LIC12345",
        )
        self.client.force_login(self.user)

    def test_dashboard_context_and_visits_counter(self):
        manufacturer = Manufacturer.objects.create(name="Bosch", country="Germany")
        category = PartCategory.objects.create(name="Brakes")
        Car.objects.create(make="Audi", model="A6", year=2020)
        Part.objects.create(
            name="Brake Pads",
            part_number="BP-001",
            price=Decimal("45.00"),
            manufacturer=manufacturer,
            category=category,
        )

        response = self.client.get(INDEX_URL)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "catalog/index.html")
        self.assertEqual(response.context["num_parts"], 1)
        self.assertEqual(response.context["num_cars"], 1)
        self.assertEqual(response.context["num_manufacturers"], 1)
        self.assertEqual(response.context["num_categories"], 1)
        self.assertEqual(response.context["num_visits"], 1)

        response2 = self.client.get(INDEX_URL)
        self.assertEqual(response2.context["num_visits"], 2)
