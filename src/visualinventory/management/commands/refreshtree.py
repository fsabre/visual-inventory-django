from django.core.management.base import BaseCommand

from visualinventory.models import Location


def recursively_apply_boundaries(obj: Location, low: int) -> int:
    """Set the low and high boundaries of a Location instance and their children."""
    obj.low = low
    high = low + 1
    for child in obj.children.all():
        high = recursively_apply_boundaries(child, high) + 1
    obj.high = high
    obj.save(update_fields=["low", "high"])
    return high


class Command(BaseCommand):
    help = "Recompute the boundaries of the locations in the tree based on their parent."

    def handle(self, *args, **kwargs):
        """Set the low and high boundaries of the locations based on their parent."""
        root = Location.objects.get(pk=1)
        recursively_apply_boundaries(root, 1)
