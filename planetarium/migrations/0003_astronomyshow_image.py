# Generated by Django 4.2.6 on 2023-11-05 17:30

from django.db import migrations, models
import planetarium.models


class Migration(migrations.Migration):
    dependencies = [
        ("planetarium", "0002_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="astronomyshow",
            name="image",
            field=models.ImageField(
                null=True, upload_to=planetarium.models.astronomy_show_image_file_path
            ),
        ),
    ]