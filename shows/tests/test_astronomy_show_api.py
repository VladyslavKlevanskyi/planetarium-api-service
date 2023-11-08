import os
import tempfile
from PIL import Image
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from shows.models import ShowTheme, AstronomyShow
from shows.serializers import (
    AstronomyShowListSerializer,
    AstronomyShowDetailSerializer,
)

ASTRONOMY_SHOW_URL = reverse("shows:astronomyshow-list")


def detail_url(astronomy_show_id):
    return reverse(
        "shows:astronomyshow-detail",
        args=[astronomy_show_id]
    )


def image_upload_url(astronomy_show_id):
    """Return URL for recipe image upload"""
    return reverse(
        "shows:astronomyshow-upload-image",
        args=[astronomy_show_id]
    )


class UnauthenticatedAstronomyShowApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        res = self.client.get(ASTRONOMY_SHOW_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class AuthenticatedAstronomyShowApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            "test@test.test",
            "testpass",
        )
        self.client.force_authenticate(self.user)

        self.show_theme1 = ShowTheme.objects.create(name="Space inside")
        self.show_theme2 = ShowTheme.objects.create(name="Space outside")
        self.show_theme3 = ShowTheme.objects.create(name="Emptiness in us")

        self.astronomy_show1 = AstronomyShow.objects.create(
            title="Good Show",
            description="Good Show description"
        )
        self.astronomy_show1.show_themes.add(self.show_theme1)

        self.astronomy_show2 = AstronomyShow.objects.create(
            title="Bad Show",
            description="Bad Show description"
        )
        self.astronomy_show2.show_themes.add(self.show_theme2)

        self.astronomy_show3 = AstronomyShow.objects.create(
            title="No match",
            description="No match show description"
        )
        self.astronomy_show3.show_themes.add(self.show_theme3)

    def test_list_astronomy_shows(self):
        res = self.client.get(ASTRONOMY_SHOW_URL)
        astronomy_shows = AstronomyShow.objects.all()
        serializer = AstronomyShowListSerializer(astronomy_shows, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_filter_astronomy_shows_by_show_themes(self):
        res = self.client.get(
            ASTRONOMY_SHOW_URL, {
                "show_themes": f"{self.show_theme1.id},{self.show_theme2.id}"
            }
        )

        serializer1 = AstronomyShowListSerializer(self.astronomy_show1)
        serializer2 = AstronomyShowListSerializer(self.astronomy_show2)
        serializer3 = AstronomyShowListSerializer(self.astronomy_show3)

        self.assertIn(serializer1.data, res.data)
        self.assertIn(serializer2.data, res.data)
        self.assertNotIn(serializer3.data, res.data)

    def test_filter_astronomy_shows_by_title(self):
        res = self.client.get(ASTRONOMY_SHOW_URL, {"title": "Show"})

        serializer1 = AstronomyShowListSerializer(self.astronomy_show1)
        serializer2 = AstronomyShowListSerializer(self.astronomy_show2)
        serializer3 = AstronomyShowListSerializer(self.astronomy_show3)

        self.assertIn(serializer1.data, res.data)
        self.assertIn(serializer2.data, res.data)
        self.assertNotIn(serializer3.data, res.data)

    def test_astronomy_show_creation_is_prohibited(self):
        payload = {
            "title": "Test Title",
            "description": "Some test description",
            "show_themes": [self.show_theme1.id]
        }
        res = self.client.post(ASTRONOMY_SHOW_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_retrieve_astronomy_show_detail(self):
        astronomy_show = AstronomyShow.objects.create(
            title="Space in us",
        )
        astronomy_show.show_themes.add(self.show_theme1)

        url = detail_url(astronomy_show.id)
        res = self.client.get(url)

        serializer = AstronomyShowDetailSerializer(astronomy_show)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)


class AdminAstronomyShowApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            "admin@admin.admin",
            "testpass",
            is_staff=True
        )
        self.client.force_authenticate(self.user)

    def test_astronomy_show_creation(self):
        show_theme1 = ShowTheme.objects.create(name="Space inside")
        show_theme2 = ShowTheme.objects.create(name="Space outside")

        payload = {
            "title": "Test Title",
            "description": "Some test description",
            "show_themes": [show_theme1.id, show_theme2.id]
        }
        res = self.client.post(ASTRONOMY_SHOW_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        astronomy_show = AstronomyShow.objects.get(id=res.data["id"])

        self.assertEqual(res.data["id"], astronomy_show.id)
        self.assertEqual(res.data["title"], astronomy_show.title)
        self.assertEqual(res.data["description"], astronomy_show.description)

        show_themes = astronomy_show.show_themes.all()

        self.assertEqual(show_themes.count(), 2)
        self.assertIn(show_theme1, show_themes)
        self.assertIn(show_theme2, show_themes)

    def test_astronomy_show_deletion(self):
        astronomy_show = AstronomyShow.objects.create(title="Best Show")
        url = detail_url(astronomy_show.id)
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)

    def test_astronomy_show_update(self):
        astronomy_show = AstronomyShow.objects.create(title="Best Show")

        show_theme = ShowTheme.objects.create(name="Space inside")
        payload = {
            "id": astronomy_show.id,
            "title": "Best Show Ever",
            "description": "Some test description",
            "show_themes": [show_theme.id],
        }

        url = detail_url(astronomy_show.id)
        res = self.client.put(url, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)

        self.assertEqual(res.data["id"], payload["id"])
        self.assertEqual(res.data["title"], payload["title"])
        self.assertEqual(res.data["description"], payload["description"])


class AstronomyShowImageUploadTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_superuser(
            "admin@myproject.com", "password"
        )
        self.client.force_authenticate(self.user)
        self.show_theme = ShowTheme.objects.create(name="Space inside")
        self.astronomy_show = AstronomyShow.objects.create(
            title="Good Show",
            description="Good Show description"
        )

    def tearDown(self):
        self.astronomy_show.image.delete()

    def test_upload_image_to_astronomy_show(self):
        """Test uploading an image to astronomy show"""
        url = image_upload_url(self.astronomy_show.id)
        with tempfile.NamedTemporaryFile(suffix=".jpg") as ntf:
            img = Image.new("RGB", (10, 10))
            img.save(ntf, format="JPEG")
            ntf.seek(0)
            res = self.client.post(url, {"image": ntf}, format="multipart")
        self.astronomy_show.refresh_from_db()

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn("image", res.data)
        self.assertTrue(os.path.exists(self.astronomy_show.image.path))

    def test_upload_image_bad_request(self):
        """Test uploading an invalid image"""
        url = image_upload_url(self.astronomy_show.id)
        res = self.client.post(url, {"image": "not image"}, format="multipart")

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_post_image_to_astronomy_show_list_should_not_work(self):
        url = ASTRONOMY_SHOW_URL
        with tempfile.NamedTemporaryFile(suffix=".jpg") as ntf:
            img = Image.new("RGB", (10, 10))
            img.save(ntf, format="JPEG")
            ntf.seek(0)

            show_theme = ShowTheme.objects.create(name="The Best Of Space")
            payload = {
                "title": "The Best Show Ever",
                "description": "Some show description",
                "show_themes": [show_theme.id],
                "image": ntf,
            }

            res = self.client.post(url, payload, format="multipart")

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        astronomy_show = AstronomyShow.objects.get(title=payload["title"])
        self.assertFalse(astronomy_show.image)

    def test_image_url_is_shown_on_astronomy_show_detail(self):
        url = image_upload_url(self.astronomy_show.id)
        with tempfile.NamedTemporaryFile(suffix=".jpg") as ntf:
            img = Image.new("RGB", (10, 10))
            img.save(ntf, format="JPEG")
            ntf.seek(0)
            self.client.post(url, {"image": ntf}, format="multipart")
        res = self.client.get(detail_url(self.astronomy_show.id))

        self.assertIn("image", res.data)

    def test_image_url_is_shown_on_astronomy_show_list(self):
        url = image_upload_url(self.astronomy_show.id)
        with tempfile.NamedTemporaryFile(suffix=".jpg") as ntf:
            img = Image.new("RGB", (10, 10))
            img.save(ntf, format="JPEG")
            ntf.seek(0)
            self.client.post(url, {"image": ntf}, format="multipart")
        res = self.client.get(ASTRONOMY_SHOW_URL)

        self.assertIn("image", res.data[0].keys())
