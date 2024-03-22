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


class Category(models.Model):
    name = models.CharField(max_length=100)
    parent = models.ForeignKey(
        to="self",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="children",
    )

    def __str__(self) -> str:
        return f"Category ({self.name})"
