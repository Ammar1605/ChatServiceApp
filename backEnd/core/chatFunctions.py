import json
from django.http import JsonResponse
from .models import Messages, ChatRoom
from django.contrib.auth.models import User

def getPeopleList(request):
    try:
        print('Here')
        sender = json.loads(request.body)['sender']
        print('sender:', sender)
        peopleList = Messages.objects.filter(sender=sender).values('receiver').distinct()
        print('peopleList:', peopleList)
        people = []
        for person in peopleList:
            print('person:', person)
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
    
def chat_history(request, room_name):
    try:
        room = ChatRoom.objects.get(name=room_name)
        messages = room.messages.order_by('timestamp').values('user__username', 'content', 'timestamp')
        return JsonResponse(list(messages), safe=False)
    except ChatRoom.DoesNotExist:
        return JsonResponse([], safe=False)
