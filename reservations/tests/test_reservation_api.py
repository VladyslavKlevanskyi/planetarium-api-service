from datetime import datetime
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from domes.models import PlanetariumDome
from shows.models import ShowTheme, AstronomyShow
from reservations.models import Reservation, ShowSession
from reservations.serializers import ReservationListSerializer

RESERVATION_URL = reverse("reservations:reservation-list")


class UnauthenticatedReservationApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        res = self.client.get(RESERVATION_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class AuthenticatedReservationApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            "test1@test1.com",
            "testpass",
        )
        self.client.force_authenticate(self.user)

    def test_list_show_reservations_for_current_user_only(self):
        user2 = get_user_model().objects.create_user(
            "test2@test2.net",
            "testpass",
        )
        Reservation.objects.create(user=self.user)
        Reservation.objects.create(user=self.user)
        Reservation.objects.create(user=user2)

        res = self.client.get(RESERVATION_URL)

        reservations_user = (Reservation.objects.order_by("-created_at")
                             .filter(user=self.user)
                             )
        serializer_user = ReservationListSerializer(
            reservations_user,
            many=True
        )
        reservations_user2 = (Reservation.objects.order_by("-created_at")
                              .filter(user=user2)
                              )
        serializer_user2 = ReservationListSerializer(
            reservations_user2,
            many=True
        )

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data["results"], serializer_user.data)

        self.client.logout()
        self.client.force_authenticate(user2)
        res2 = self.client.get(RESERVATION_URL)
        self.assertEqual(res2.data["results"], serializer_user2.data)

    def test_reservation_creation(self):
        show_theme = ShowTheme.objects.create(name="Emptiness in us")

        astronomy_show = AstronomyShow.objects.create(
            title="Good Show",
            description="Good Show description"
        )
        astronomy_show.show_themes.add(show_theme)

        planetarium_dome = PlanetariumDome.objects.create(
            name="Dome Name",
            rows=10,
            seats_in_row=10,
        )

        date = datetime(
            year=2023,
            month=3,
            day=1,
            hour=10,
            minute=0,
            second=0,
        )

        show_session = ShowSession.objects.create(
            astronomy_show=astronomy_show,
            planetarium_dome=planetarium_dome,
            show_time=date
        )

        payload = {
            "tickets": [
                {
                    "row": 3,
                    "seat": 5,
                    "show_session": show_session.id
                }
            ]
        }

        res = self.client.post(RESERVATION_URL, payload, format="json")

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(
            res.data["tickets"][0]["row"],
            payload["tickets"][0]["row"]
        )
        self.assertEqual(
            res.data["tickets"][0]["seat"],
            payload["tickets"][0]["seat"]
        )
        self.assertEqual(
            res.data["tickets"][0]["show_session"],
            payload["tickets"][0]["show_session"]
        )
