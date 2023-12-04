from django.db import models


class CartItem(models.Model):
    cart = models.ForeignKey(
        "Cart", on_delete=models.CASCADE, related_name="users_cart")
    collectible = models.ForeignKey(
        "Collectible", on_delete=models.CASCADE, related_name="item_in_cart")
    quantity = models.IntegerField(null=True, blank=True)
