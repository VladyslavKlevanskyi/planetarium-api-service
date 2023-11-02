from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from planetarium.models import PlanetariumDome
from planetarium.serializers import (
    PlanetariumDomeSerializer
)

PLANETARIUM_DOME_URL = reverse("planetarium:planetariumdome-list")


def detail_url(planetarium_dome_id):
    return reverse(
        "planetarium:planetariumdome-detail",
        args=[planetarium_dome_id]
    )


class UnauthenticatedPlanetariumDomeApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        res = self.client.get(PLANETARIUM_DOME_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class AuthenticatedPlanetariumDomeApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            "test@test.test",
            "testpass",
        )
        self.client.force_authenticate(self.user)

        for planetarium_dome_index in range(1, 4):
            PlanetariumDome.objects.create(
                name=f"Dome {planetarium_dome_index}",
                rows=planetarium_dome_index,
                seats_in_row=planetarium_dome_index,
            )

    def test_list_planetarium_domes(self):
        res = self.client.get(PLANETARIUM_DOME_URL)
        planetarium_domes = PlanetariumDome.objects.all()
        serializer = PlanetariumDomeSerializer(planetarium_domes, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_planetarium_dome_creation_is_prohibited(self):
        payload = {
            "name": "Big Dome",
            "rows": 5,
            "seats_in_row": 1,
        }
        res = self.client.post(PLANETARIUM_DOME_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)


class AdminPlanetariumDomeApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            "admin@admin.admin",
            "testpass",
            is_staff=True
        )
        self.client.force_authenticate(self.user)

    def test_planetarium_dome_creation(self):
        payload = {
            "name": "Big Dome",
            "rows": 5,
            "seats_in_row": 1,
        }
        res = self.client.post(PLANETARIUM_DOME_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        planetarium_dome = PlanetariumDome.objects.get(id=res.data["id"])

        self.assertEqual(res.data["id"], planetarium_dome.id)
        self.assertEqual(res.data["name"], planetarium_dome.name)
        self.assertEqual(res.data["rows"], planetarium_dome.rows)
        self.assertEqual(
            res.data["seats_in_row"],
            planetarium_dome.seats_in_row
        )

    def test_planetarium_dome_deletion(self):
        planetarium_dome = PlanetariumDome.objects.create(
            name="Dome Test",
            rows=2,
            seats_in_row=3,
        )

        url = detail_url(planetarium_dome.id)
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)

    def test_planetarium_dome_update(self):
        planetarium_dome = PlanetariumDome.objects.create(
            name="Dome Test",
            rows=2,
            seats_in_row=3,
        )
        payload = {
            "id": planetarium_dome.id,
            "name": "Big Dome",
            "rows": 5,
            "seats_in_row": 1,
        }

        url = detail_url(planetarium_dome.id)
        res = self.client.put(url, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)

        self.assertEqual(res.data["id"], payload["id"])
        self.assertEqual(res.data["name"], payload["name"])
        self.assertEqual(res.data["rows"], payload["rows"])
        self.assertEqual(res.data["seats_in_row"], payload["seats_in_row"])
