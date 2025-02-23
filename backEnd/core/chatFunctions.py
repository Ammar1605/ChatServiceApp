import json
from django.http import JsonResponse
from .models import Messages
from django.contrib.auth.models import User

def getPeopleList(request):
    try:
        sender = json.loads(request.body)['sender']
        peopleList = Messages.objects.filter(sender=sender).values('receiver').distinct()
        people = []
        for person in peopleList:
            tmp = User.objects.get(username=person['receiver'])
            people.append({
                'username': tmp.username,
                'email': tmp.email,
                'name': tmp.first_name,
                'surname': tmp.last_name
            })
        print(people)

        return JsonResponse({'status': 'OK', 'peopleList': list(people)})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)