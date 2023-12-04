from django.db import models


class Favorite(models.Model):
    user = models.ForeignKey(
        "PixoUser", on_delete=models.CASCADE, related_name="favorites")
    collectible = models.ForeignKey(
        "Collectible", on_delete=models.CASCADE, related_name="favorited_by")
