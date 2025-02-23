from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
import json

# Function for login of user
# @param request: request object
# @return: OK if successful, invalid credentials if unsuccessful, method not allowed if method is not POST
def userLogin(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        email = data['email']
        username = User.objects.get(email=email).username
        password = data['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return JsonResponse({'status': 'OK'})
        else:
            return JsonResponse({'status': 'Invalid credentials'}, status=401)
    return JsonResponse({'status': 'Method not allowed'}, status=405)

# Function for getting user details
# @param request: request object
# @return: user details if successful, method not allowed if method is not GET or if user is not logged in
@login_required
def getUserDetails(request):
    user = request.user
    if user: 
        return JsonResponse({
            'status': 'OK',
            'user': {
                'username': user.username,
                'email': user.email,
                'name': user.first_name,
                'surname': user.last_name
            }
        })
    else:
        return JsonResponse({'status': 'User not logged in'}, status=401)

# Function for logout of user
# @param request: request object
# @return: OK if successful, method not allowed if method is not POST or if user is not logged in
def userLogout(request):
    if request.method == 'POST':
        logout(request)
        return JsonResponse({'status': 'OK'})
    return JsonResponse({'status': 'Method not allowed'}, status=405)