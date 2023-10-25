from django.conf import settings
from django.db import models


class ShowTheme(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


class AstronomyShow(models.Model):
    title = models.CharField(max_length=255, unique=True)
    description = models.TextField()
    show_themes = models.ManyToManyField(
        ShowTheme,
        related_name="astronomy_shows"
    )

