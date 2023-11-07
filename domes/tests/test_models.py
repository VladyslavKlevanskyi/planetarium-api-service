from django.test import TestCase
from planetarium.models import PlanetariumDome

PLANETARIUM_DOME_NAME = "Planetarium Dome Name"


class PlanetariumDomeModelTests(TestCase):
    def test_str_and_capacity_in_planetarium_dome_model(self):
        data = {
            "name": PLANETARIUM_DOME_NAME,
            "rows": 6,
            "seats_in_row": 10,
        }
        calc_capacity = data["rows"] * data["seats_in_row"]
        planetarium_dome = PlanetariumDome.objects.create(
            name=data["name"],
            rows=data["rows"],
            seats_in_row=data["seats_in_row"]
        )

        self.assertEqual(
            str(planetarium_dome),
            f"{planetarium_dome.name} (capacity: {calc_capacity})"
        )
