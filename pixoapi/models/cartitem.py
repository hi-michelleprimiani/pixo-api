from django.db import models


class CartItem(models.Model):
    user = models.ForeignKey(
        "PixoUser", on_delete=models.CASCADE, related_name="carts")
    collectible = models.ForeignKey(
        "Collectible", on_delete=models.CASCADE, related_name="collectibles")
    quantity = models.IntegerField()
