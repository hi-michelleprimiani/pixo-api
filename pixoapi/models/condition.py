from django.db import models


class Condition(models.Model):
    condition = models.CharField()
