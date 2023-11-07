from datetime import datetime
from unittest import mock
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.test import TestCase
from domes.models import PlanetariumDome
from planetarium.models import AstronomyShow, ShowTheme
from reservations.models import Reservation, ShowSession, Ticket

SHOW_THEME_NAME = "Test Show Theme"
ASTRONOMY_SHOW_TITLE = "Test Astronomy Show"
ASTRONOMY_SHOW_DESCRIPTION = "Astronomy Show Description"

PLANETARIUM_DOME_NAME = "Planetarium Dome Name"

USER_EMAIL = "test@test.com"
USER_PASSWORD = "TestPass"


class ReservationModelTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            email=USER_EMAIL,
            password=USER_PASSWORD,
        )

        self.mocked1 = datetime(
            year=2022,
            month=2,
            day=24,
            hour=14,
            minute=45,
            second=0,
        )
        self.mocked2 = datetime(
            year=2022,
            month=2,
            day=24,
            hour=14,
            minute=50,
            second=0,
        )
        self.mocked3 = datetime(
            year=2022,
            month=2,
            day=24,
            hour=14,
            minute=55,
            second=0,
        )
        with mock.patch(
                "django.utils.timezone.now",
                mock.Mock(return_value=self.mocked1)
        ):
            self.reservation1 = Reservation.objects.create(user=self.user)
        with mock.patch(
                "django.utils.timezone.now",
                mock.Mock(return_value=self.mocked2)
        ):
            self.reservation2 = Reservation.objects.create(user=self.user)
        with mock.patch(
                "django.utils.timezone.now",
                mock.Mock(return_value=self.mocked3)
        ):
            self.reservation3 = Reservation.objects.create(user=self.user)

    def test_str_in_reservation_model(self):

        self.assertEqual(
            str(self.reservation1),
            f"{str(self.mocked1)} by: {self.reservation1.user}"
        )

    def test_ordering_in_reservation_model(self):
        ordering_list = []
        for reservation in Reservation.objects.all():
            ordering_list.append(reservation.created_at)

        self.assertEqual(
            ordering_list,
            [
                self.reservation3.created_at,
                self.reservation2.created_at,
                self.reservation1.created_at
            ]
        )


class ShowSessionModelTests(TestCase):
    def setUp(self):
        self.astronomy_show = AstronomyShow.objects.create(
            title=ASTRONOMY_SHOW_TITLE,
            description=ASTRONOMY_SHOW_DESCRIPTION
        )
        planetarium_dome = PlanetariumDome.objects.create(
            name=PLANETARIUM_DOME_NAME,
            rows=4,
            seats_in_row=6
        )
        self.session_list = []
        for i in range(1, 4):
            session = ShowSession.objects.create(
                astronomy_show=self.astronomy_show,
                planetarium_dome=planetarium_dome,
                show_time=datetime(
                    year=2024,
                    month=2,
                    day=24,
                    hour=18,
                    minute=i,
                    second=0
                )
            )
            self.session_list.append(session)

    def test_str_in_show_session_model(self):
        show_session = ShowSession.objects.get(id=self.session_list[0].id)
        self.assertEqual(
            str(show_session),
            f"{show_session.astronomy_show.title} {show_session.show_time}"
        )

    def test_ordering_in_show_session_model(self):
        ordering_list = []
        for session in ShowSession.objects.all():
            ordering_list.append(session)

        self.assertEqual(ordering_list, self.session_list)

    def test_fields_in_show_session_model(self):
        show_session = ShowSession.objects.get(id=self.session_list[0].id)

        self.assertEqual(
            show_session.astronomy_show.title,
            ASTRONOMY_SHOW_TITLE
        )
        self.assertEqual(
            show_session.planetarium_dome.name,
            PLANETARIUM_DOME_NAME
        )
        self.assertEqual(
            show_session.show_time,
            self.session_list[0].show_time
        )


class TicketTests(TestCase):
    def setUp(self):
        show_theme = ShowTheme.objects.create(name=SHOW_THEME_NAME)
        astronomy_show = AstronomyShow.objects.create(
            title=ASTRONOMY_SHOW_TITLE,
            description=ASTRONOMY_SHOW_DESCRIPTION
        )
        astronomy_show.show_themes.add(show_theme)
        planetarium_dome = PlanetariumDome.objects.create(
            name=PLANETARIUM_DOME_NAME,
            rows=5,
            seats_in_row=15
        )
        user = get_user_model().objects.create_user(
            email=USER_EMAIL,
            password=USER_PASSWORD,
        )
        self.reservation = Reservation.objects.create(user=user)
        self.show_session = ShowSession.objects.create(
            astronomy_show=astronomy_show,
            planetarium_dome=planetarium_dome,
            show_time=datetime(
                year=2022,
                month=3,
                day=3,
                hour=4,
                minute=1,
                second=0,
            )
        )

        self.ticket = Ticket.objects.create(
            show_session=self.show_session,
            reservation=self.reservation,
            row=1,
            seat=2
        )

    def test_str_in_ticket_model(self):
        self.assertEqual(
            str(self.ticket),
            f"{str(self.ticket.show_session)}"
            f" (row: {self.ticket.row}, seat: {self.ticket.seat})"
        )

    def test_ordering_in_ticket_model(self):
        ticket1 = Ticket.objects.create(
            show_session=self.show_session,
            reservation=self.reservation,
            row=4,
            seat=4
        )
        ticket2 = Ticket.objects.create(
            show_session=self.show_session,
            reservation=self.reservation,
            row=2,
            seat=4
        )
        ticket3 = Ticket.objects.create(
            show_session=self.show_session,
            reservation=self.reservation,
            row=3,
            seat=4
        )
        ticket4 = Ticket.objects.create(
            show_session=self.show_session,
            reservation=self.reservation,
            row=2,
            seat=3
        )

        self.assertEqual(
            list(Ticket.objects.all()),
            [self.ticket, ticket4, ticket2, ticket3, ticket1]
        )

    def test_fields_in_ticket_model(self):
        self.assertEqual(
            self.ticket.show_session.astronomy_show.title,
            ASTRONOMY_SHOW_TITLE
        )
        self.assertEqual(
            self.ticket.reservation.user.email,
            USER_EMAIL
        )
        self.assertEqual(self.ticket.row, 1)
        self.assertEqual(self.ticket.seat, 2)

    def test_validation_in_ticket_model(self):
        message = "Validation method doesn't work"
        try:
            Ticket.objects.create(
                show_session=self.show_session,
                reservation=self.reservation,
                row=100,
                seat=100
            )

        except ValidationError:
            message = "Validation method works"

        self.assertEqual(message, "Validation method works")
