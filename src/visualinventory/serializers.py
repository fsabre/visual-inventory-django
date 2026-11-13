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
        fields = ["id", "name", "parent", "children", "categories", "x", "y", "dx", "dy"]

    children = serializers.SerializerMethodField()
    categories = serializers.SerializerMethodField()

    def get_children(self, obj) -> None:
        """Return None, to indicate that no children will be returned, even if there are."""
        return None

    def get_categories(self, obj: Location):
        return CategorySerializer(obj.get_recursive_categories(), many=True).data


class LocationSerializer(LocationWithoutChildrenSerializer):
    """The base serializer for Locations."""

    # Define the additional fields exposed by the serializer.
    class Meta(LocationWithoutChildrenSerializer.Meta):
        fields = LocationWithoutChildrenSerializer.Meta.fields + ["search_result"]

    # This is supposed to be a ListField, but it just doesn't work.
    children = serializers.ListSerializer(child=LocationWithoutChildrenSerializer())
    search_result = serializers.SerializerMethodField()

    def get_fields(self):
        """Remove search_result from the serialized fields when no search parameter is provided."""

        fields = super().get_fields()

        request = self.context.get("request")
        if request is None or "search" not in request.query_params:
            fields.pop("search_result", None)

        return fields

    def get_search_result(self, obj: Location):
        """Return the IDs of all recursive children matching the requested category."""

        request = self.context.get("request")
        category_id = request.query_params.get("search") # None, blank or str
        try:
            category_id = int(category_id)
        except ValueError:
            return []

        locations = obj.get_recursive_children().filter(stored_categories__id=category_id)
        return list(locations.values_list("id", flat=True).distinct())


class CategorySerializer(serializers.ModelSerializer):
    """The base serializer for Categories."""

    class Meta:
        model = Category
        fields = ["id", "name"]
