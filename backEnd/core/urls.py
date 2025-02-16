from django.urls import path
from . import views, apiFunctions

urlpatterns = [
    path('getcsrf', views.getcsrf, name='csrf'),
    path('ping', views.ping_pong, name='Ping Pong'),
    path('login', apiFunctions.userLogin, name='Login'),
    path('checkLogin', apiFunctions.getUserDetails, name='Check Login'),
    path('logout', apiFunctions.userLogout, name='Logout'),
]