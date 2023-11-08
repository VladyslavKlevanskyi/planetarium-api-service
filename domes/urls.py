from django.urls import path, include
from rest_framework import routers
from domes.views import PlanetariumDomeViewSet

router = routers.DefaultRouter()
router.register("domes", PlanetariumDomeViewSet)

urlpatterns = [
    path("", include(router.urls))
]

app_name = "domes"
