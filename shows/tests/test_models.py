from django.test import TestCase
from shows.models import AstronomyShow, ShowTheme

SHOW_THEME_NAME = "Test Show Theme"
ASTRONOMY_SHOW_TITLE = "Test Astronomy Show"
ASTRONOMY_SHOW_DESCRIPTION = "Astronomy Show Description"


class ShowThemeModelTests(TestCase):
    def test_str_in_show_theme_model(self):
        show_theme = ShowTheme.objects.create(name=SHOW_THEME_NAME)
        self.assertEqual(str(show_theme), f"{show_theme.name}")


class AstronomyShowModelTests(TestCase):
    def test_fields_in_astronomy_show_model(self):
        show_theme = ShowTheme.objects.create(name=SHOW_THEME_NAME)

        astronomy_show = AstronomyShow.objects.create(
            title=ASTRONOMY_SHOW_TITLE,
            description=ASTRONOMY_SHOW_DESCRIPTION
        )
        astronomy_show.show_themes.add(show_theme)

        self.assertEqual(
            astronomy_show.title,
            ASTRONOMY_SHOW_TITLE
        )
        self.assertEqual(
            astronomy_show.description,
            ASTRONOMY_SHOW_DESCRIPTION
        )
        self.assertEqual(
            astronomy_show.show_themes.get(name=SHOW_THEME_NAME),
            show_theme
        )
