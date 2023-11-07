from datetime import datetime
from django.db.models import Count, F
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from domes.models import PlanetariumDome
from planetarium.models import (
    ShowTheme,
    AstronomyShow,
    ShowSession,
)
from planetarium.serializers import (
    ShowSessionListSerializer,
    ShowSessionDetailSerializer,
)

SHOW_SESSION_URL = reverse("planetarium:showsession-list")


def detail_url(show_session_id):
    return reverse(
        "planetarium:showsession-detail",
        args=[show_session_id]
    )


class UnauthenticatedShowSessionApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        res = self.client.get(SHOW_SESSION_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class AuthenticatedShowSessionApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            "test@test.test",
            "testpass",
        )
        self.client.force_authenticate(self.user)

        show_theme = ShowTheme.objects.create(name="Space inside")

        self.astronomy_show = AstronomyShow.objects.create(
            title="Good Show",
            description="Good Show description"
        )
        self.astronomy_show.show_themes.add(show_theme)
        self.planetarium_dome = PlanetariumDome.objects.create(
            name="Dome Test",
            rows=2,
            seats_in_row=3,
        )

        for time_index in range(1, 4):
            ShowSession.objects.create(
                astronomy_show=self.astronomy_show,
                planetarium_dome=self.planetarium_dome,
                show_time=datetime(
                    year=2022,
                    month=3,
                    day=time_index,
                    hour=14,
                    minute=0,
                    second=0,
                )
            )

    def test_list_show_sessions(self):
        res = self.client.get(SHOW_SESSION_URL)
        show_sessions = ShowSession.objects.order_by("show_time").annotate(
            tickets_available=(
                F("planetarium_dome__rows")
                * F("planetarium_dome__seats_in_row")
                - Count("tickets")
            )
        )
        serializer = ShowSessionListSerializer(show_sessions, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_filter_show_sessions_by_date(self):
        date = datetime(
            year=2023,
            month=3,
            day=1,
            hour=10,
            minute=0,
            second=0,
        )

        ShowSession.objects.create(
            astronomy_show=self.astronomy_show,
            planetarium_dome=self.planetarium_dome,
            show_time=date
        )
        ShowSession.objects.create(
            astronomy_show=self.astronomy_show,
            planetarium_dome=self.planetarium_dome,
            show_time=date
        )

        queryset = ShowSession.objects.annotate(
            tickets_available=(
                F("planetarium_dome__rows")
                * F("planetarium_dome__seats_in_row")
                - Count("tickets")
            )
        ).filter(show_time__date=date)

        res = self.client.get(
            SHOW_SESSION_URL,
            {"date": "2023-03-01"}
        )
        serializer = ShowSessionListSerializer(queryset, many=True)

        self.assertEqual(serializer.data, res.data)

    def test_filter_show_sessions_by_astronomy_show(self):
        show_theme = ShowTheme.objects.create(name="Dark Space")

        astronomy_show = AstronomyShow.objects.create(
            title="Very Good Show",
            description="Very Good Show description"
        )
        astronomy_show.show_themes.add(show_theme)

        date = datetime(
            year=2023,
            month=3,
            day=1,
            hour=10,
            minute=0,
            second=0,
        )

        ShowSession.objects.create(
            astronomy_show=astronomy_show,
            planetarium_dome=self.planetarium_dome,
            show_time=date
        )
        ShowSession.objects.create(
            astronomy_show=astronomy_show,
            planetarium_dome=self.planetarium_dome,
            show_time=date
        )

        queryset = ShowSession.objects.annotate(
            tickets_available=(
                F("planetarium_dome__rows")
                * F("planetarium_dome__seats_in_row")
                - Count("tickets")
            )
        ).filter(astronomy_show_id=astronomy_show.id)

        res = self.client.get(
            SHOW_SESSION_URL,
            {"astronomy_show": astronomy_show.id}
        )
        serializer = ShowSessionListSerializer(queryset, many=True)

        self.assertEqual(serializer.data, res.data)

    def test_show_session_creation_is_prohibited(self):
        date = datetime(
            year=2033,
            month=3,
            day=1,
            hour=10,
            minute=0,
            second=0,
        )

        payload = {
            "astronomy_show": self.astronomy_show.id,
            "planetarium_dome": self.planetarium_dome.id,
            "show_time": date
        }
        res = self.client.post(SHOW_SESSION_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_retrieve_astronomy_show_detail(self):
        show_theme = ShowTheme.objects.create(name="Dark Space")

        astronomy_show = AstronomyShow.objects.create(
            title="Very Good Show",
            description="Very Good Show description"
        )
        astronomy_show.show_themes.add(show_theme)

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
            planetarium_dome=self.planetarium_dome,
            show_time=date
        )

        url = detail_url(show_session.id)
        res = self.client.get(url)

        serializer = ShowSessionDetailSerializer(show_session)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)


class AdminShowSessionApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            "test@test.test",
            "testpass",
            is_staff=True
        )
        self.client.force_authenticate(self.user)

        show_theme = ShowTheme.objects.create(name="Space inside")

        self.astronomy_show = AstronomyShow.objects.create(
            title="Good Show",
            description="Good Show description"
        )
        self.astronomy_show.show_themes.add(show_theme)
        self.planetarium_dome = PlanetariumDome.objects.create(
            name="Dome Test",
            rows=2,
            seats_in_row=3,
        )

        for time_index in range(1, 4):
            ShowSession.objects.create(
                astronomy_show=self.astronomy_show,
                planetarium_dome=self.planetarium_dome,
                show_time=datetime(
                    year=2022,
                    month=3,
                    day=time_index,
                    hour=14,
                    minute=0,
                    second=0,
                )
            )

    def test_show_session_creation(self):
        date = datetime(
            year=2033,
            month=3,
            day=1,
            hour=10,
            minute=0,
            second=0,
        )

        payload = {
            "astronomy_show": self.astronomy_show.id,
            "planetarium_dome": self.planetarium_dome.id,
            "show_time": date
        }
        res = self.client.post(SHOW_SESSION_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        show_session = ShowSession.objects.get(id=res.data["id"])
        self.assertEqual(res.data["id"], show_session.id)
        self.assertEqual(
            res.data["astronomy_show"],
            show_session.astronomy_show.id
        )
        self.assertEqual(
            res.data["planetarium_dome"],
            show_session.planetarium_dome.id
        )
