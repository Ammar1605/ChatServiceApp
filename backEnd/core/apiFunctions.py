from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
import json

# Function for login of user
# @param request: request object
# @return: 0 if successful, 1 if unsuccessful
def userLogin(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        email = data['email']
        username = User.objects.get(email=email).username
        # username = 'aminacordic'
        print(username)
        password = data['password']
        print(password)
        user = authenticate(request, username=username, password=password)
        print(user)
        if user is not None:
            login(request, user)
            return JsonResponse({'status': 'OK'})
        else:
            return JsonResponse({'status': 'Invalid credentials'}, status=401)
    return JsonResponse({'status': 'Method not allowed'}, status=405)

@login_required
def getUserDetails(request):
    user = request.user
    return JsonResponse({
        'status': 'OK',
        'user': {
            'username': user.username,
            'email': user.email,
            'name': user.first_name,
            'surname': user.last_name,
            # Add any other user details you want to return
        }
    })

# Function for logout of user
# @param request: request object
# @return: 0 if successful, 1 if unsuccessful
def userLogout(request):
    if request.method == 'POST':
        logout(request)
        return JsonResponse({'status': 'OK'})
    return JsonResponse({'status': 'Method not allowed'}, status=405)