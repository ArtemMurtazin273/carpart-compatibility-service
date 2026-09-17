from django.test import Client, TestCase
from django.urls import reverse


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
