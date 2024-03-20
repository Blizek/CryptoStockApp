from rest_framework.test import APITestCase
from django.urls import reverse
from faker import Faker


class TestSetUp(APITestCase):

    def setUp(self):
        self.register_url = reverse("register")
        self.login_url = reverse("login")
        self.fake = Faker()

        self.user_data = {
            "name": self.fake.name().split()[0],
            "surname": self.fake.name().split()[1],
            "email": self.fake.email(),
            "date_of_birth": self.fake.date(),
            "sex": "MALE",
            "password": self.fake.name(),
        }

        return super().setUp()

    def tearDown(self):
        return super().tearDown()
