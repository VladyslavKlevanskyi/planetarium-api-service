# Generated by Django 4.2.6 on 2023-11-08 11:29

from django.db import migrations, models
import shows.models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="ShowTheme",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=255, unique=True)),
            ],
            options={
                "ordering": ["id"],
            },
        ),
        migrations.CreateModel(
            name="AstronomyShow",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("title", models.CharField(max_length=255, unique=True)),
                ("description", models.TextField()),
                (
                    "image",
                    models.ImageField(
                        null=True, upload_to=shows.models.astronomy_show_image_file_path
                    ),
                ),
                (
                    "show_themes",
                    models.ManyToManyField(
                        related_name="astronomy_shows", to="shows.showtheme"
                    ),
                ),
            ],
            options={
                "ordering": ["id"],
            },
        ),
    ]