from django.urls import path, include
from rest_framework import routers
from shows.views import (
    ShowThemeViewSet,
    AstronomyShowViewSet,
)

router = routers.DefaultRouter()
router.register("show-themes", ShowThemeViewSet)
router.register("astronomy-shows", AstronomyShowViewSet)

urlpatterns = [
    path("", include(router.urls))
]

app_name = "shows"
