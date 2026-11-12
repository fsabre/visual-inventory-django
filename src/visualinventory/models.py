from typing import Iterable

from django.db import models, transaction
from django.core.exceptions import ValidationError
from django.db.models import F


class Location(models.Model):
    """
    Represents a location within the inventory structure.
    Locations are organized as a tree, where each location can have a parent and multiple children.
    Each location also stores its position and dimensions, which are used for its graphical
    representation.
    The hierarchy is managed using the Nested Set Model, where 'low' and 'high'
    define each location's interval. Locations are not deleted to avoid the overhead of updating
    intervals. Gaps in interval values are tolerated and do not affect the hierarchy.
    """

    name = models.CharField(max_length=100)
    parent = models.ForeignKey(
        to="self",
        null=True,  # The field can be null (for the initial space)
        blank=False,  # But it can't be blank (as newly created Location must have a parent)
        on_delete=models.CASCADE,
        related_name="children",
    )
    x = models.IntegerField(blank=True)
    y = models.IntegerField(blank=True)
    dx = models.IntegerField(default=32)
    dy = models.IntegerField(default=32)

    high = models.PositiveIntegerField(blank=True)
    low = models.PositiveIntegerField(blank=True)

    class Meta:
        constraints = [
            models.CheckConstraint(condition=models.Q(dx__gt=0), name="positive_dx"),
            models.CheckConstraint(condition=models.Q(dy__gt=0), name="positive_dy"),
            models.CheckConstraint(condition=models.Q(high__gt=0), name="positive_high"),
            models.CheckConstraint(condition=models.Q(low__gt=0), name="positive_low"),
        ]

    def set_auto_position_x(self) -> int:
        """Find an available x position to avoid collision with others locations"""
        if self.parent_id is None:
            return 0

        # Find sibling locations
        siblings = Location.objects.filter(parent_id=self.parent_id)
        siblings = siblings.exclude(pk=self.pk)
        boxes = list(siblings.values_list("x", "y", "dx", "dy"))

        x = 0
        y = self.y
        # Search for an available x position
        while True:
            # Check whether the current position collide with any siblings
            for bx, by, bdx, bdy in boxes:
                collision = x < bx + bdx and x + self.dx > bx and y < by + bdy and y + self.dy > by
                # If a collision is detected, move x to the sibling's right edge
                if collision:
                    x = bx + bdx
                    break
            # Return the first x position without any collision
            else:
                return x

    def __str__(self) -> str:
        return self.name

    def clean(self) -> None:
        super().clean()

        if self.y is None:
            self.y = 0
        if self.x is None:
            self.x = self.set_auto_position_x()

        # Ensure the parent validation is ran only when the instance is
        # created/the parent change.
        if self.pk:
            previous_parent_id = Location.objects.only("parent_id").get(pk=self.pk).parent_id
            if previous_parent_id != self.parent_id:
                self.validate_parent()
                self.move(self.parent)
        else:
            self.set_up_intervals()

    def set_up_intervals(self) -> None:
        """Set up a basic interval for newly added locations."""
        low: int = self.parent.high
        Location.objects.filter(low__gte=low).update(low=F("low") + 2)
        Location.objects.filter(high__gte=low).update(high=F("high") + 2)
        self.low = low
        self.high = self.low + 1

    def move(self, new_parent: "Location") -> None:
        """Update the database with the new parent and intervals."""
        with transaction.atomic():  # I AM ATOMIC
            self.parent = new_parent
            self.save(update_fields=["parent"])
            destination_low: int = new_parent.high
            subtree_size: int = self.high - self.low + 1
            # Create the interval space at the destination
            Location.objects.filter(low__gte=destination_low).update(low=F("low") + subtree_size)
            Location.objects.filter(high__gte=destination_low).update(high=F("high") + subtree_size)
            # If you move the location to a smaller index, reserving a space will shift the location
            # interval.
            self.refresh_from_db(fields=["low", "high"])
            source_low: int = self.low
            movement_diff: int = destination_low - source_low
            # Move the whole subtree
            (
                Location.objects.filter(low__gte=self.low, high__lte=self.high).update(
                    low=F("low") + movement_diff, high=F("high") + movement_diff
                )
            )
            # Suppress the initial space at the source
            Location.objects.filter(low__gte=source_low).update(low=F("low") - subtree_size)
            Location.objects.filter(high__gte=source_low).update(high=F("high") - subtree_size)
        self.refresh_from_db(fields=["low", "high"])

    def validate_parent(self) -> None:
        """Raise an ValidationError if the change in parent breaks the tree."""

        if self.parent.low >= self.low and self.parent.high <= self.high:
            raise ValidationError("A location cannot be in itself or its own descendants")

    def get_recursive_children(self) -> Iterable["Location"]:
        query = Location.objects.filter(
            low__gt=self.low,
            high__lt=self.high,
        )
        return query

    def get_recursive_categories(self) -> Iterable["Category"]:
        query = Category.objects.filter(
            locations__in=self.get_recursive_children()
        ).distinct()
        return query


class Category(models.Model):
    name = models.CharField(max_length=100)
    locations = models.ManyToManyField(Location, blank=True, related_name="stored_categories")

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self) -> str:
        return self.name
