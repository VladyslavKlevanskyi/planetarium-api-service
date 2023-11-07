from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet
from domes.models import PlanetariumDome
from domes.serializers import PlanetariumDomeSerializer
from planetarium.permissions import IsAdminOrIfAuthenticatedReadOnly


class PlanetariumDomeViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    mixins.UpdateModelMixin,
    GenericViewSet,
):
    queryset = PlanetariumDome.objects.all()
    serializer_class = PlanetariumDomeSerializer
    permission_classes = (IsAdminOrIfAuthenticatedReadOnly,)
