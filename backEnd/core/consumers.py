import json
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        from .models import ChatRoom
        print('Connection request')
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        print(self.room_name)
        self.room_group_name = f"chat_{self.room_name}"
        print(self.room_group_name)

        # Create or get the chat room from the database
        self.chat_room = await sync_to_async(ChatRoom.objects.get_or_create)(name=self.room_name)

        # Join room group
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        print('Connection closed: ', self.room_group_name)
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        from .models import Messages
        data = json.loads(text_data)
        message = data['message']
        sender = data['sender']
        receiver = data['receiver']
        print('Message received: ', message)
        print('Message sent: ', sender)

        # Save the message to the database
        # Using sync_to_async to call the synchronous ORM code in an async context
        await sync_to_async(Messages.objects.create)(
            room=self.chat_room[0],  # get_or_create returns a tuple (object, created)
            message=message,
            sender=sender, 
            receiver=receiver,
            is_sent=True
        )

        # Broadcast message to the group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
            }
        )

    async def chat_message(self, event):
        message = event['message']
        await self.send(text_data=json.dumps({'message': event['message']}))
