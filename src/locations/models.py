from typing import Set

from django.db import models


class Location(models.Model):
    name = models.CharField(max_length=100)
    parent = models.ForeignKey(
        to="self",
        null=True,  # The field can be null (for the initial space)
        blank=False,  # But it can't be blank (as newly created Location must have a parent)
        on_delete=models.CASCADE,
        related_name="children",
    )

    def __str__(self) -> str:
        return f"Location ({self.name})"

    def fill_with_category_names(self, s: Set[str]) -> None:
        """Fill a set with all category names in this location and its sub-locations."""
        s.update(self.stored_categories.values_list("name", flat=True))
        for sub_location in self.children.all():
            sub_location.fill_with_category_names(s)


class Category(models.Model):
    name = models.CharField(max_length=100)
    locations = models.ManyToManyField(Location, related_name="stored_categories")

    def __str__(self) -> str:
        return f"Category ({self.name})"
