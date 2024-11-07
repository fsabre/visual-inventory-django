from typing import Dict, Iterable

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
        return self.name

    def to_json(self, depth: int = 0, include_categories: bool = False) -> Dict:
        content = {
            "id": self.id,
            "name": self.name,
            "parent": self.parent.id if self.parent else None,
            "children": [],
        }
        if include_categories:
            content["categories"] = [cat.to_json() for cat in self.get_recursive_categories()]
        if depth > 0:
            for child in self.children.all():
                child_data = child.to_json(depth=depth - 1, include_categories=include_categories)
                content["children"].append(child_data)
        return content

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
    locations = models.ManyToManyField(Location, related_name="stored_categories")

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self) -> str:
        return self.name

    def to_json(self) -> Dict:
        content = {
            "id": self.id,
            "name": self.name,
        }
        return content
