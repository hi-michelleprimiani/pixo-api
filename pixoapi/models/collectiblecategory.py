from django.db import models


class CollectibleCategory(models.Model):
    category = models.ForeignKey("Category", on_delete=models.CASCADE)
    collectible = models.ForeignKey("Collectible", on_delete=models.CASCADE)
