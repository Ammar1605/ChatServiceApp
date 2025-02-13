from django.urls import path
from . import views

urlpatterns = [
    path('ping', views.ping_pong, name='Ping Pong')
]