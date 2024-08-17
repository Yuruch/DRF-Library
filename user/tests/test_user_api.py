from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model

USER = get_user_model()


class RegistrationTests(APITestCase):
    def setUp(self):
        self.register_url = reverse("user:create")

    def test_user_registration(self):
        new_user_data = {
            "email": "newuser@example.com",
            "password": "newpassword123",
            "first_name": "New",
            "last_name": "User"
        }
        response = self.client.post(self.register_url, new_user_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(USER.objects.count(), 1)
        self.assertEqual(USER.objects.get(email=new_user_data["email"]).email, new_user_data["email"])


class UserTests(APITestCase):
    def setUp(self):
        self.register_url = reverse("user:create")
        self.token_url = reverse("user:token_obtain_pair")
        self.manage_url = reverse("user:manage")
        self.user_data = {
            "email": "testuser@example.com",
            "password": "testpassword123",
            "first_name": "Test",
            "last_name": "User"
        }
        self.user = USER.objects.create_user(**self.user_data)
        self.client.force_authenticate(user=self.user)

    def test_manage_user(self):
        response = self.client.get(self.manage_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["email"], self.user_data["email"])

    def test_update_user(self):
        old_password_hash = self.user.password
        response = self.client.patch(self.manage_url, {
            "first_name": "Updated",
            "password": "newpassword123"
        }, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertEqual(self.user.first_name, "Updated")
        self.assertTrue(self.user.check_password("newpassword123"))
        self.assertNotEqual(self.user.password, old_password_hash)
        self.assertTrue(self.user.password.startswith("pbkdf2_sha256$"))

class UserLoginTests(APITestCase):
    def setUp(self):
        self.token_url = reverse("user:token_obtain_pair")
        self.user_data = {
            "email": "testuser@example.com",
            "password": "testpassword123",
            "first_name": "Test",
            "last_name": "User"
        }
        self.user = USER.objects.create_user(**self.user_data)

    def test_user_login_successful(self):
        response = self.client.post(self.token_url, {
            "email": self.user_data["email"],
            "password": self.user_data["password"]
        }, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)
        self.assertTrue(response.data["access"])
        self.assertTrue(response.data["refresh"])
