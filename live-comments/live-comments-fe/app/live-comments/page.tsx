'use client'
import { socket } from './client_socket';
import { get, post } from './api_requests';
import Hero from './hero';
import { useState, useEffect } from 'react';
import io from 'socket.io-client';
import axios from 'axios';

const BE_SERVER = "http://localhost:8000"
const CHANNELS = [
  {
    id: 1,
    name: "cooking",
    messages: ["hello", "world"]
  },
  {
    id: 2,
    name: "dancing",
    messages: ["lorem", "ipsum"]
  }
]
const URLS = {
  "new_message":   `${BE_SERVER}/live-comments/comments/new`,
  "past_messages": `${BE_SERVER}/live-comments/comments/past`
}
const Message = () => {
    const [currentMessage, setCurrentMessage] = useState("")
    const [currentChannel, setChannel]   = useState(1)
    const [messages, setMessages] = useState([])

    const setCurrentChannel = (channel_key) => {
      setChannel(channel_key.split("_")[1])
    };

    useEffect(() => {

      get(URLS.new_message, { "channel_id": currentChannel })
      socket.connect()
      socket.on("connect", onConnect)
      socket.on('message_channel_1', receiveMessage);
      return () => {
        socket.disconnect();
      };
    }, []);

    const sendMessage = () => {
      const payload = {
          "channel_id" : channel,
          "comment": currentMessage,
          "user_id": "1", //hardcoded
          "user_ts": (new Date()).getTime(),
      }
      const onError = () => {}
      const onSuccess = () => setCurrentMessage("")

      post(URLS.new_message, payload, onSuccess, onError)
    };

    const receiveMessage = (message) => {
      console.log("RECEIVED", message)
      const channel = 
      const channel_id = message.channel_id;


      // setMessages((prevMessages) => [...prevMessages, message]);
    };
    const onConnect = () => { console.log("CONNECTED TO SERVER ⚡️🔌")}

    return (
        // <div>
      <Hero
        channels={CHANNELS}
        currentChannel={channel}
        currentMessage={currentMessage}
        setCurrentMessage={setCurrentMessage}
        setCurrentChannel={setCurrentChannel}
        sendMessage={sendMessage}
      />
    );
};

export default Message;