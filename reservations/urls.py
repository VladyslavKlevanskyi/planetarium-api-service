from django.urls import path, include
from rest_framework import routers
from reservations.views import ReservationViewSet, ShowSessionViewSet

router = routers.DefaultRouter()
router.register("reservations", ReservationViewSet)
router.register("show-sessions", ShowSessionViewSet)

urlpatterns = [
    path("", include(router.urls))
]

app_name = "reservations"
