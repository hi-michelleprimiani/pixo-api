from django.db import models


class Category(models.Model):
    label = models.CharField()
    collectibles = models.ManyToManyField(
        "Collectible", through='CollectibleCategory', related_name='categories')
