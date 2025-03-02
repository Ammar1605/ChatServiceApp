import json, hashlib
from django.contrib.auth.models import User
from django.db.models import Q
from django.http import JsonResponse
from .models import Messages, ChatRoom

""" def getPeopleList(request):
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
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500) """

def getPeopleList(request):
    try:
        current_user = json.loads(request.body)['sender']
        qs_sender = Messages.objects.filter(sender=current_user).exclude(receiver='').values_list('receiver', flat=True).distinct()
        qs_receiver = Messages.objects.filter(receiver=current_user).exclude(sender='').values_list('sender', flat=True).distinct()
        partners = list(qs_sender.union(qs_receiver))
        print(partners)
        people = []
        for person in partners:
            print('person:', person)
            tmp = User.objects.get(username=person)
            people.append({
                'username': tmp.username,
                'email': tmp.email,
                'name': tmp.first_name,
                'surname': tmp.last_name
            })
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

def getMessages(request):
    try:
        """ sender = json.loads(request.body)['sender']
        receiver = json.loads(request.body)['receiver'] """
        room_name = json.loads(request.body)['room']
        pager = json.loads(request.body)['page']
        print('pager:', pager)
        messages = Messages.objects.filter(room__name=room_name)
        if messages:
            messages = messages.values('sender', 'receiver', 'message', 'file', 'timestamp').order_by('-timestamp')
            messages = messages[:(50*pager)][::-1]
            return JsonResponse(list(messages), safe=False)
        else:
            return JsonResponse([], safe=False)
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
    
def getRoomName(request):
    try:
        sender = json.loads(request.body)['sender']
        receiver = json.loads(request.body)['receiver']
        # room = ChatRoom.objects.filter(participants__username=sender).filter(participants__username=receiver)
        # search for a room that has both sender and receiver
        room = ChatRoom.objects.filter(participants__contains=sender).filter(participants__contains=receiver)
        print('sender:', sender)
        print('receiver:', receiver)
        print('room:', room)
        if room.exists():
            return JsonResponse({'status': 'OK', 'room': room[0].name})
        else:
            room_name = hashlib.md5(f'{sender}_{receiver}'.encode()).hexdigest()
            return JsonResponse({'status': 'OK', 'room': room_name})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)