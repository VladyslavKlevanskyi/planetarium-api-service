from django.urls import path, include
from rest_framework import routers
from planetarium.views import (
    ShowThemeViewSet,
    AstronomyShowViewSet,
    ShowSessionViewSet,
    ReservationViewSet,
)

router = routers.DefaultRouter()
router.register("show-themes", ShowThemeViewSet)
router.register("astronomy-shows", AstronomyShowViewSet)
router.register("show-sessions", ShowSessionViewSet)
router.register("reservations", ReservationViewSet)

urlpatterns = [
    path("", include(router.urls))
]

app_name = "planetarium"
