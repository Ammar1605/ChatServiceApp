from django.http import JsonResponse
from django.middleware.csrf import get_token
from django.shortcuts import render

# Create your views here.
def ping_pong(request):
    return JsonResponse({'status': 'PONG'})

def getcsrf(request):
    if request.method == 'GET':
        csrf_token = get_token(request)
        return JsonResponse({'csrfToken': csrf_token})
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)