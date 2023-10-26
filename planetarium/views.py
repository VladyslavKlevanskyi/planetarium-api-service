from rest_framework import viewsets

from planetarium.models import (
    ShowTheme,
)
from planetarium.serializers import (
    ShowThemeSerializer,
)


class ShowThemeViewSet(viewsets.ModelViewSet):
    queryset = ShowTheme.objects.all()
    serializer_class = ShowThemeSerializer
