from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from planetarium.models import ShowTheme
from planetarium.serializers import ShowThemeSerializer

SHOW_THEME_URL = reverse("planetarium:showtheme-list")


def sample_show_theme(*names):
    for name in [*names]:
        ShowTheme.objects.create(name=name)


def detail_url(show_theme_id):
    return reverse("planetarium:showtheme-detail", args=[show_theme_id])


class UnauthenticatedShowThemeApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        res = self.client.get(SHOW_THEME_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class AuthenticatedShowThemeApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            "test@test.test",
            "testpass",
        )
        self.client.force_authenticate(self.user)

    def test_list_show_themes(self):
        sample_show_theme("name1", "name2", "name3")
        res = self.client.get(SHOW_THEME_URL)
        show_themes = ShowTheme.objects.order_by("id")
        serializer = ShowThemeSerializer(show_themes, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_show_theme_creation_is_prohibited(self):
        payload = {
            "name": "Test Name",
        }
        res = self.client.post(SHOW_THEME_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)


class AdminShowThemeApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            "admin@admin.com",
            "testpass",
            is_staff=True
        )
        self.client.force_authenticate(self.user)

    def test_show_theme_creation(self):
        payload = {
            "name": "Test Name",
        }
        res = self.client.post(SHOW_THEME_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        show_theme = ShowTheme.objects.get(id=res.data["id"])
        for key in payload.keys():
            self.assertEqual(payload[key], getattr(show_theme, key))

    def test_show_theme_deletion(self):
        show_theme = ShowTheme.objects.create(name="test name")
        url = detail_url(show_theme.id)

        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
