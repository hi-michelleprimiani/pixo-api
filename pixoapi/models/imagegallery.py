from django.db import models


class ImageGallery(models.Model):
    collectible = models.ForeignKey(
        "Collectible", on_delete=models.CASCADE, related_name="image_gallery")
    image = models.ForeignKey(
        "Image", on_delete=models.CASCADE, related_name="image_collection")
