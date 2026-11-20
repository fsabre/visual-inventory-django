from django.db import transaction
from django.db.models import OuterRef, Exists
from rest_framework import serializers

from .models import Category, Location


class TinyLocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = ["id", "name"]


class LocationWithoutChildrenSerializer(serializers.ModelSerializer):
    """Same as the LocationSerializer, but with null instead of a children list.
    To reduce code duplication, LocationSerializer inherit this class.
    """

    class Meta:
        model = Location
        fields = [
            "id",
            "name",
            "parent",
            "children",
            "categories",
            "descendant_categories",
            "x",
            "y",
            "dx",
            "dy",
        ]

    children = serializers.SerializerMethodField()
    categories = serializers.SerializerMethodField()
    descendant_categories = serializers.SerializerMethodField()

    def get_children(self, obj: Location) -> None:
        """ "Return None, because this field won't be filled in this lesser serializer."""
        return None

    def get_categories(self, obj: Location) -> None:
        """ "Return None, because this field won't be filled in this lesser serializer."""
        return None

    def get_descendant_categories(self, obj: Location) -> None:
        """ "Return None, because this field won't be filled in this lesser serializer."""
        return None


class LocationSerializer(LocationWithoutChildrenSerializer):
    """The base serializer for Locations."""

    # Define the additional fields exposed by the serializer
    class Meta(LocationWithoutChildrenSerializer.Meta):
        fields = LocationWithoutChildrenSerializer.Meta.fields + ["search_result"]

    search_result = serializers.SerializerMethodField()

    def get_fields(self):
        """Remove search_result from the serialized fields when no search parameter is provided."""
        fields = super().get_fields()
        request = self.context.get("request")
        if request is None or "search" not in request.query_params:
            fields.pop("search_result", None)
        return fields

    def get_children(self, obj: Location):
        """Return immediate children in a more lightweight format."""
        return LocationWithoutChildrenSerializer(obj.children.all(), many=True).data

    def get_categories(self, obj: Location):
        """Return immediate categories."""
        return CategorySerializer(obj.stored_categories.all(), many=True).data

    def get_descendant_categories(self, obj: Location):
        """Return all categories from descendant locations."""
        return CategorySerializer(obj.get_descendant_categories(), many=True).data

    def get_search_result(self, obj: Location):
        """Return IDs of descendants matching the requested category."""
        request = self.context.get("request")
        category_id = request.query_params.get("search")
        try:
            category_id = int(category_id)
        except ValueError:
            return []

        # Subquery to find locations matching the requested category
        matching_locations = Location.objects.filter(
            stored_categories__id=category_id,
            low__gte=OuterRef("low"),
            high__lte=OuterRef("high"),
        )

        # Retrieve descendants of the current location that contain
        # at least one matching location from the subquery
        locations = (
            Location.objects.filter(
                low__gte=obj.low,
                high__lte=obj.high,
            ).annotate(
                contains_matching_location=Exists(matching_locations)
            ).filter(contains_matching_location=True)
        )

        return locations.values_list("id", flat=True)


class LocationCreateSerializer(serializers.ModelSerializer):
    """A serializer to create new Locations"""

    class Meta:
        model = Location
        fields = ["name", "parent", "x", "y", "dx", "dy"]
        extra_kwargs = {
            "dx": {"min_value": 1},
            "dy": {"min_value": 1},
        }

    @transaction.atomic
    def create(self, validated_data):
        location = Location(**validated_data)
        location.full_clean()
        location.save()
        return location


class CategorySerializer(serializers.ModelSerializer):
    """The base serializer for Categories."""

    class Meta:
        model = Category
        fields = ["id", "name"]
