import { writable } from 'svelte/store';

const XOR_KEY = import.meta.env.VITE_XOR_KEY || 'default-xor-key';

export const messages = writable([]);
export let socket;

export function connect(roomName) {
  socket = new WebSocket(`ws://chatservice.local:8000/ws/chat/${roomName}/`);

  socket.onopen = () => console.log('WebSocket connection established.');

  socket.onmessage = (event) => {
    console.log('Received message:', event.data);
    const data = JSON.parse(xorDecrypt(event.data));
    showNotification(data.sender, data.message);
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
    socket.send(xorEncryptDecrypt(JSON.stringify(data)));
  }
}

function xorEncryptDecrypt(data) {
  let jsonString = JSON.stringify(data);
  let encrypted = '';

  for (let i = 0; i < jsonString.length; i++) {
      encrypted += String.fromCharCode(jsonString.charCodeAt(i) ^ XOR_KEY.charCodeAt(i % XOR_KEY.length));
  }

  // Convert encrypted string to Base64 to make it safe for transmission
  return btoa(encrypted);
}

function xorDecrypt(encryptedData) {
  // Decode Base64 first
  let decoded = atob(encryptedData);
  let decrypted = '';

  for (let i = 0; i < decoded.length; i++) {
      decrypted += String.fromCharCode(decoded.charCodeAt(i) ^ XOR_KEY.charCodeAt(i % XOR_KEY.length));
  }
  console.log('Decrypted:', decrypted);
  // Convert back to JSON object
  return JSON.parse(decrypted);
}

function showNotification(sender, message) {
  if (Notification.permission === "granted") {
    new Notification(`New message from ${sender}`, {
      body: message,
      icon: "/favicon.png", // Replace with your app icon
    });
  } else if (Notification.permission !== "denied") {
    Notification.requestPermission().then((permission) => {
      if (permission === "granted") {
        showNotification(sender, message);
      }
    });
  }

}