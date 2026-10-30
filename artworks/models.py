from django.db import models
from django.db.models import Max
from django.db.models.deletion import PROTECT


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


class Artwork(models.Model):
    """
    Stores an individual artwork belonging to a collection.
    """

    title = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(
        max_length=220,
        unique=True,
    )
    collection = models.ForeignKey(
        Collection,
        on_delete=PROTECT,
        related_name="artworks",
    )
    year = models.PositiveIntegerField(
        blank=True,
        null=True,
    )
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to="artworks/")
    etsy_url = models.URLField(max_length=300, blank=True)
    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["etsy_url"],
                condition=~models.Q(etsy_url=""),
                name="unique_non_empty_etsy_url",
            ),
        ]

    def __str__(self):
        return self.title
