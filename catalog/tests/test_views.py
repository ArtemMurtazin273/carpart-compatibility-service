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


class PartViewsTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = get_user_model().objects.create_user(
            username="lead_mechanic",
            password="securepassword123",
            license_number="MEC99999",
        )
        self.client.force_login(self.user)

        self.manufacturer = Manufacturer.objects.create(name="Brembo", country="Italy")
        self.category = PartCategory.objects.create(name="Braking")

    def test_parts_pagination(self):
        for i in range(7):
            Part.objects.create(
                name=f"Part {i}",
                part_number=f"BR-{i:03d}",
                price=Decimal("100.00"),
                manufacturer=self.manufacturer,
                category=self.category,
            )

        response = self.client.get(PARTS_URL)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["part_list"]), 5)
        self.assertTrue(response.context["is_paginated"])

    def test_part_search_by_name(self):
        Part.objects.create(
            name="Oil Filter High Flow",
            part_number="OF-100",
            price=Decimal("15.00"),
            manufacturer=self.manufacturer,
            category=self.category,
        )
        Part.objects.create(
            name="Brake Disc Front",
            part_number="BD-200",
            price=Decimal("120.00"),
            manufacturer=self.manufacturer,
            category=self.category,
        )

        response = self.client.get(PARTS_URL, {"name": "Filter"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["part_list"]), 1)
        self.assertEqual(response.context["part_list"][0].name, "Oil Filter High Flow")

    def test_toggle_assign_mechanic_to_part(self):
        part = Part.objects.create(
            name="Spark Plug Platinum",
            part_number="SP-300",
            price=Decimal("12.50"),
            manufacturer=self.manufacturer,
            category=self.category,
        )
        toggle_url = reverse("catalog:toggle-part-assign", args=[part.id])

        response = self.client.get(toggle_url)
        self.assertRedirects(response, reverse("catalog:part-detail", args=[part.id]))
        self.assertIn(self.user, part.mechanics.all())

        response = self.client.get(toggle_url)
        self.assertRedirects(response, reverse("catalog:part-detail", args=[part.id]))
        self.assertNotIn(self.user, part.mechanics.all())
