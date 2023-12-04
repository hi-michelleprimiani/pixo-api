from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class UserReview(models.Model):
    reviewer = models.ForeignKey(
        "PixoUser", on_delete=models.CASCADE, related_name="reviews_given")
    target_user = models.ForeignKey(
        "PixoUser", on_delete=models.CASCADE, related_name="reviews_received")
    rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)])
    comment = models.CharField(max_length=500)
    review_date = models.DateTimeField(auto_now_add=True)
