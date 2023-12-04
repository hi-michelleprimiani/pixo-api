from django.db import models


class Condition(models.Model):
    title = models.CharField(max_length=300, null=True)
    description = models.CharField(max_length=300, null=True)
