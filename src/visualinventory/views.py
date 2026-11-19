from typing import Type

from rest_framework import viewsets
from rest_framework.serializers import Serializer

from .models import Location, Category
from .serializers import TinyLocationSerializer, LocationSerializer, CategorySerializer, LocationCreateSerializer

from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet

from rest_framework.permissions import IsAuthenticated, IsAdminUser

class LocationViewSet(mixins.CreateModelMixin,
                   mixins.RetrieveModelMixin,
                   mixins.ListModelMixin,
                   GenericViewSet):
    queryset = Location.objects.all()

    def get_permissions(self):
        if self.action == "list":
            return [IsAuthenticated()]
        if self.action == "create":
            return [IsAdminUser()]
        return []
    
    def get_serializer_class(self) -> Type[Serializer]:
        if self.action == "retrieve":
            return LocationSerializer
        if self.action == "create":
            return LocationCreateSerializer
        return TinyLocationSerializer


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
