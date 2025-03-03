from django.contrib import admin
from .models import Messages, ChatRoom, LoginHistory

# Register your models here.
admin.site.register(Messages)
admin.site.register(ChatRoom)
admin.site.register(LoginHistory)