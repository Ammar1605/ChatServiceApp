from django.db import models
from django.conf import settings
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
    
# Create your models here.
class ChatRoom(models.Model):
    name = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    # Optionally, add a list of participants if your chat is private or group-based:
    participants = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True)

    def __str__(self):
        return self.name

class Messages(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE, related_name='messages', default='')
    message = models.TextField()
    sender = models.CharField(null=True, blank=True, default='', max_length=100)
    receiver = models.CharField(null=True, blank=True, default='', max_length=100)
    is_read = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)
    is_sent = models.BooleanField(default=False)
    is_received = models.BooleanField(default=False)
    is_delivered = models.BooleanField(default=False)
