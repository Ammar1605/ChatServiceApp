from django.db import models
from django.conf import settings
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
    
# Create your models here.
class ChatRoom(models.Model):
    name = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    participants = models.TextField()

    def __str__(self):
        return self.name

class Messages(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE, related_name='messages', default='')
    message = models.TextField()
    file = models.CharField(null=True, blank=True, default='', max_length=255)
    sender = models.CharField(null=True, blank=True, default='', max_length=100)
    receiver = models.CharField(null=True, blank=True, default='', max_length=100)
    is_read = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)
    is_sent = models.BooleanField(default=False)
    is_received = models.BooleanField(default=False)
    is_delivered = models.BooleanField(default=False)

class LoginHistory(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    ip_address = models.GenericIPAddressField()
    user_agent = models.CharField(max_length=255)
    recordType = models.CharField(max_length=255, default='login')
