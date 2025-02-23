from django.db import models

# Create your models here.
class Messages(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    message = models.TextField()
    sender = models.CharField(max_length=100)
    receiver = models.CharField(max_length=100)
    is_read = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)
    is_sent = models.BooleanField(default=False)
    is_received = models.BooleanField(default=False)
    is_delivered = models.BooleanField(default=False)
    