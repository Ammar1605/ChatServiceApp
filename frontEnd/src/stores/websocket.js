import { writable } from 'svelte/store';

export const messages = writable([]);
export let socket;

export function connect(roomName) {
  socket = new WebSocket(`ws://chatservice.local:8000/ws/chat/${roomName}/`);

  socket.onopen = () => console.log('WebSocket connection established.');

  socket.onmessage = (event) => {
    const data = JSON.parse(event.data);
    messages.update(msgs => [...msgs, data.message]);
  };

  socket.onclose = () => console.log('WebSocket closed.');

  return socket;
}

export function sendMessage(message, sender, receiver) {
  if (socket.readyState === WebSocket.OPEN) {
    socket.send(JSON.stringify({ message, sender, receiver }));
  }
}
