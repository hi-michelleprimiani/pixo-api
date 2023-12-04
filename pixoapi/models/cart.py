from django.db import models


class Cart(models.Model):
    user = models.ForeignKey(
        "PixoUser", on_delete=models.CASCADE, related_name="carts")
    purchase_date = models.DateTimeField(null=True, blank=True)
    paid = models.BooleanField(default=False)
    items = models.ManyToManyField(
        "Collectible", through='CartItem', related_name="carts")
