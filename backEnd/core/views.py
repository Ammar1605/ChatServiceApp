from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
def ping_pong(request):
    return JsonResponse({'status': 'PONG'})