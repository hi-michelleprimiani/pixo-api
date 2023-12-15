from django.db import models


class Message(models.Model):
    sender = models.ForeignKey(
        "PixoUser", on_delete=models.CASCADE, related_name="outgoing_message")
    receiver = models.ForeignKey(
        "PixoUser", on_delete=models.CASCADE, related_name="incoming_message")
    text = models.CharField(max_length=10000)
    date_time = models.DateTimeField(auto_now_add=True)
