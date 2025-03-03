import json, hashlib, ast
from django.contrib.auth.models import User
from django.db.models import Q
from django.http import JsonResponse
from .models import Messages, ChatRoom

def getPeopleList(request):
    try:
        current_user = json.loads(request.body)['sender']
        partners = ChatRoom.objects.filter(participants__contains=current_user).values_list('participants', flat=True)
        people = []
        for partner in partners:
            partner = ast.literal_eval(partner)
            if partner[0] == current_user:
                partner = partner[1]
            else:
                partner = partner[0]
            tmp = User.objects.get(username=partner)
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

        if room.exists():
            return JsonResponse({'status': 'OK', 'room': room[0].name})
        else:
            room_name = hashlib.md5(f'{sender}_{receiver}'.encode()).hexdigest()
            chat_room, created = ChatRoom.objects.get_or_create(name=room_name, participants=f"['{sender}', '{receiver}']")
            return JsonResponse({'status': 'OK', 'room': room_name, 'existing': True if created or chat_room else False})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
    
def searchPeople(request):
    try:
        search = json.loads(request.body)['query']
        users = User.objects.filter(Q(username__icontains=search) | Q(first_name__icontains=search) | Q(last_name__icontains=search))
        people = []
        for person in users:
            people.append({
                'username': person.username,
                'email': person.email,
                'name': person.first_name,
                'surname': person.last_name
            })
        return JsonResponse({'status': 'OK', 'people': list(people)})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)