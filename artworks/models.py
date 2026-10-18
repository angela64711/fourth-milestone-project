from django.db import models


class Collection(models.Model):
    """
    Stores an artwork collection that can be assigned to artworks.
    """

    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=120, unique=True)
    description = models.TextField()
    display_order = models.PositiveIntegerField(
        blank=True,
        null=True,
        editable=False,
    )

    class Meta:
        ordering = ["display_order", "id"]

    def save(self, *args, **kwargs):
        """
        Assigns the next display position to new collections.
        """
        if self.pk is None and self.display_order is None:
            max_order = Collection.objects.aggregate(Max("display_order"))[
                "display_order__max"
            ]

            if max_order is None:
                self.display_order = 1
            else:
                self.display_order = max_order + 1

        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
