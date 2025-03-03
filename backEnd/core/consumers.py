import base64, json, os
from asgiref.sync import sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer

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
        data = await self.xor_decrypt(text_data)
        data = json.loads(data)
        message = data['message']
        sender = data['sender']
        receiver = data['receiver']
        file_data = data['file']

        if message != '' or file_data != '':
            if file_data != '':
                file_name = file_data['name']
                file_content = base64.b64decode(file_data['content'])
                file_path = f'/home/ammar/ChatServiceApp/frontEnd/static/sharedFiles/{file_name}'
                if os.path.exists(file_path):
                    i = 0
                    while True:
                        new_file_path = f'/home/ammar/ChatServiceApp/frontEnd/static/sharedFiles/{file_name[:-4]} ({i}){file_name[-4:]}'
                        if not os.path.exists(new_file_path):
                            file_path = new_file_path
                            file_name = f'{file_name[:-4]} ({i}){file_name[-4:]}'
                            file_data['name'] = file_name
                            break
                        i += 1
                with open(file_path, 'wb') as file:
                    file.write(file_content)


            # Save the message to the database
            # Using sync_to_async to call the synchronous ORM code in an async context
            await sync_to_async(Messages.objects.create)(
                room=self.chat_room[0],  # get_or_create returns a tuple (object, created)
                message=message,
                file='' if not file_data else file_name,
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
                    'file': file_data,
                    'sender': sender,
                    'receiver': receiver
                }
            )

    async def xor_encrypt_decrypt(self, data, decrypt=False):
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

    async def xor_decrypt(self, encrypted_data):
        xor_key = os.getenv("XOR_KEY", "default-xor-key")

        # Decode Base64
        encrypted_data = base64.b64decode(encrypted_data).decode()

        # XOR operation to decrypt
        decrypted_data = ''.join(
            chr(ord(encrypted_data[i]) ^ ord(xor_key[i % len(xor_key)]))
            for i in range(len(encrypted_data))
        )

        return json.loads(decrypted_data)  # Convert back to dictionary


    async def chat_message(self, event):
        message = event['message']
        file_data = event['file']
        sender = event['sender']
        receiver = event['receiver']
        message = json.dumps({'message':message,'file':file_data,'sender':sender,'receiver':receiver})
        message = await self.xor_encrypt_decrypt(message)
        await self.send(text_data=message)
