from django.db import models


class Collectible(models.Model):
    seller = models.ForeignKey(
        "PixoUser", on_delete=models.CASCADE, related_name="seller_collectibles")
    name = models.CharField(max_length=300)
    description = models.CharField(max_length=10000)
    price = models.DecimalField(decimal_places=2, max_digits=7)
    material = models.CharField(max_length=300)
    color = models.CharField(max_length=300, null=True, blank=True)
    size = models.CharField(max_length=300)
    created_date = models.DateTimeField(auto_now_add=True)
    categories = models.ManyToManyField(
        "Category", through='CollectibleCategory', related_name='collectibles')
    images = models.ManyToManyField(
        "Image", through="ImageGallery", related_name="collectibles")
