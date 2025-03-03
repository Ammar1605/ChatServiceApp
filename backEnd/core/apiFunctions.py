from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from .models import LoginHistory
import json, base64, os

# Function for login of user
# @param request: request object
# @return: OK if successful, invalid credentials if unsuccessful, method not allowed if method is not POST
def userLogin(request):
    if request.method == 'POST':
        data = json.loads(xor_decrypt(request.body))
        email = data['email']
        username = User.objects.get(email=email).username
        password = data['password']
        user = authenticate(request, username=username, password=password)
        print(user)
        if user is not None:
            login(request, user)
            LoginHistory.objects.create(
                user=user,
                ip_address=request.META.get('HTTP_X_REAL_IP'),
                user_agent=request.META.get('HTTP_USER_AGENT'),
                recordType='login'
            )
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

def xor_encrypt_decrypt(data, decrypt=False):
    xor_key = os.getenv("XOR_KEY", "default-xor-key")

    if not decrypt:
        # Convert dictionary to JSON string
        data = json.dumps(data)

    # XOR operation
    encrypted_data = ''.join(
        chr(ord(data[i]) ^ ord(xor_key[i % len(xor_key)]))
        for i in range(len(data))
    )

    if decrypt:
        return json.loads(encrypted_data)  # Convert back to dictionary

    # Encode encrypted text in Base64 to ensure safe transmission
    return base64.b64encode(encrypted_data.encode()).decode()

def xor_decrypt(encrypted_data):
    xor_key = os.getenv("XOR_KEY", "default-xor-key")

    # Decode Base64
    encrypted_data = base64.b64decode(encrypted_data).decode()

    # XOR operation to decrypt
    decrypted_data = ''.join(
        chr(ord(encrypted_data[i]) ^ ord(xor_key[i % len(xor_key)]))
        for i in range(len(encrypted_data))
    )

    return json.loads(decrypted_data)  # Convert back to dictionary