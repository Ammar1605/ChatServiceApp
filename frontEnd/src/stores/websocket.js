import { writable } from 'svelte/store';

export const messages = writable([]);
export let socket;

export function connect(roomName) {
  socket = new WebSocket(`ws://chatservice.local:8000/ws/chat/${roomName}/`);

  socket.onopen = () => console.log('WebSocket connection established.');

  socket.onmessage = (event) => {
    const data = JSON.parse(event.data);
    messages.update(msgs => {
      console.log('Message:');
      console.log(msgs);
      console.log('Data:');
      console.log(data);

      const lastMessage = msgs[msgs.length - 1];
      if (lastMessage != data) {
        let newMsg = {
          message: data.message,
          file: data.file.name,
          sender: data.sender,
          receiver: data.receiver,
        };
        return [...msgs, newMsg];
      }
      return msgs;
    });
  };

  socket.onclose = () => {
    console.log('WebSocket closed.');
    // try reconnect 5 times with 5 seconds delay if the connection is closed
    /* for (let i = 0; i < 5; i++) {
      socket = new WebSocket(`ws://chatservice.local:8000/ws/chat/${roomName}/`);
      if (socket.readyState === WebSocket.OPEN) {
        break;
      }
      setTimeout(() => {
        console.log('Reconnecting...');
      }, 5000);
    }*/
  } 
  return socket; 
}

export function sendMessage(message, sender, receiver, file=null) {
  if (socket.readyState === WebSocket.OPEN) {
    const data = { message, sender, receiver };
    data.file = file == null ? '' : file;
    socket.send(JSON.stringify(data));
  }
}
