from typing import Type

from rest_framework import viewsets
from rest_framework.serializers import Serializer

from .models import Location, Category
from .serializers import TinyLocationSerializer, LocationSerializer, CategorySerializer


class LocationViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Location.objects.all()

    def get_serializer_class(self) -> Type[Serializer]:
        if self.action == "retrieve":
            return LocationSerializer
        return TinyLocationSerializer


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
