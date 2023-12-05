from django.db import models


class Image(models.Model):
    img_url = models.URLField()
