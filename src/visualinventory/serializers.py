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
        fields = ["id", "name", "parent", "children", "categories"]

    children = serializers.SerializerMethodField()
    categories = serializers.SerializerMethodField()

    def get_children(self, obj) -> None:
        """Return None, to indicate that no children will be returned, even if there are."""
        return None

    def get_categories(self, obj: Location):
        return CategorySerializer(obj.get_recursive_categories(), many=True).data


class LocationSerializer(LocationWithoutChildrenSerializer):
    """The base serializer for Locations."""

    # This is supposed to be a ListField, but it just doesn't work.
    children = serializers.ListSerializer(child=LocationWithoutChildrenSerializer())


class CategorySerializer(serializers.ModelSerializer):
    """The base serializer for Categories."""

    class Meta:
        model = Category
        fields = ["id", "name"]
