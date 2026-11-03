from typing import Iterable

from django.db import models
from django.core.exceptions import ValidationError


class Location(models.Model):
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
                collision = (x < bx + bdx and x + self.dx > bx
                             and y < by + bdy and y + self.dy > by)
                # If a collision is detected, move x to the sibling's right edge
                if collision:
                    x = bx + bdx
                    break
            # Return the first x position without any collision
            else:
                return x  


    class Meta:
        constraints = [
            models.CheckConstraint(condition=models.Q(dx__gt=0), name="positive_dx"),
            models.CheckConstraint(condition=models.Q(dy__gt=0), name="positive_dy"),
        ]

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
        else:
            self.validate_parent()

    def validate_parent(self) -> None:
        """Raise an ValidationError if the change in parent breaks the tree."""

        if self == self.parent:
            raise ValidationError("A location cannot be its own parent")
        current_parent = self.parent
        while current_parent is not None:
            if current_parent == self:
                raise ValidationError("A location cannot be in its own descendants")
            current_parent = current_parent.parent

    def get_recursive_children(self) -> Iterable["Location"]:
        query = Location.objects.raw(
            raw_query="""WITH RECURSIVE children AS (
                SELECT id, name, parent_id from visualinventory_location WHERE id == %(self_id)s
                UNION ALL
                SELECT l.id, l.name, l.parent_id from visualinventory_location l, children WHERE l.parent_id == children.id
            )
            SELECT * from children""",
            params={"self_id": self.id},
        )
        return query

    def get_recursive_categories(self) -> Iterable["Category"]:
        query = Category.objects.filter(locations__in=self.get_recursive_children()).distinct()
        return query


class Category(models.Model):
    name = models.CharField(max_length=100)
    locations = models.ManyToManyField(Location, blank=True, related_name="stored_categories")

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self) -> str:
        return self.name
