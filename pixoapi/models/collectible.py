from django.db import models


class Collectible(models.Model):
    seller_id = models.ForeignKey(
        "PixoUser", on_delete=models.CASCADE, related_name="seller_collectibles")
    name = models.CharField(max_length=300)
    description = models.CharField(max_length=1000)
    price = models.DecimalField(decimal_places=2, max_digits=7)
    quantity = models.IntegerField(default=1, null=True, blank=True)
    material = models.CharField(max_length=300)
    size = models.CharField(max_length=300)
    condition = models.ForeignKey(
        "Condition", on_delete=models.CASCADE, related_name="items")
    created_date = models.DateTimeField(auto_now_add=True)
    categories = models.ManyToManyField(
        "Category", through='CollectibleCategory', related_name='collectibles')
