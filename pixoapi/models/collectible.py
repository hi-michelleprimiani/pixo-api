from django.db import models


class Collectible(models.Model):
    seller_id = models.ForeignKey(
        "PixoUser", on_delete=models.CASCADE, related_name="seller_collectibles")
    name = models.CharField()
    description = models.CharField(max_length=1000)
    price = models.DecimalField(decimal_places=2, max_digits=7)
    quantity = models.IntegerField(default=1)
    img_url = models.URLField()
    material = models.CharField()
    size = models.CharField()
    condition = models.ForeignKey(
        "Condition", on_delete=models.CASCADE, related_name="items")
    created_date = models.DateTimeField(auto_now_add=True)
