from django.db import models
from django.contrib.auth.models import User


class PixoUser(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="pixo_user")
    bio = models.CharField(max_length=1000, blank=True)
    location = models.CharField(max_length=300, null=False)
    img_url = models.URLField()
    created_on = models.DateField(auto_now_add=True)
