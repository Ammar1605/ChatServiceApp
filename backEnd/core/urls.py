from django.urls import path
from . import views, apiFunctions, chatFunctions

urlpatterns = [
    path('getcsrf', views.getcsrf, name='csrf'),
    path('ping', views.ping_pong, name='Ping Pong'),
    path('login', apiFunctions.userLogin, name='Login'),
    path('checkLogin', apiFunctions.getUserDetails, name='Check Login'),
    path('logout', apiFunctions.userLogout, name='Logout'),
    path('getPeopleList', chatFunctions.getPeopleList, name='Get People List'),
    path('searchPeople', chatFunctions.searchPeople, name='Search People'),
    path('getMessages', chatFunctions.getMessages, name='Get Messages'),
    path('getRoomName', chatFunctions.getRoomName, name='Get Room Name'),
]