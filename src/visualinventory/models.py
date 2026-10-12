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
    x = models.IntegerField(default=0)
    y = models.IntegerField(default=0)
    dx = models.IntegerField(default=32)
    dy = models.IntegerField(default=32)

    class Meta:
        constraints = [
            models.CheckConstraint(condition=models.Q(dx__gt=0), name="positive_dx"),
            models.CheckConstraint(condition=models.Q(dy__gt=0), name="positive_dy"),
        ]

    def __str__(self) -> str:
        return self.name

    def clean(self) -> None:
        super().clean()

        # Ensure the parent validation is ran only when the instance is
        # created/the parent change.
        if self.pk:
            previous_parent_id = Location.objects.only("parent_id").get(pk=self.pk).parent_id
            if previous_parent_id == self.parent_id:
                return

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
