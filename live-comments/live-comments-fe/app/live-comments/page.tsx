'use client'
import { socket } from './client_socket';
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

const Message = () => {
    const [channels, setChannel] = useState(CHANNELS);
    const [currentMessage, setCurrentMessage] = useState("")
    const [currentChannel, setCurrentChannel] = useState("dancing_2")

    useEffect(() => {
      socket.connect()
      socket.on("connect", onConnect)
      socket.on('message_channel_', receiveMessage);
      return () => {
        socket.disconnect();
      };
    }, []);

    const sendMessage = () => {
        axios.post(`${BE_SERVER}/live-comments/comment`, {
            "channel_id" : 1,
            "comment": currentMessage,
            "user_id": "1", //hardcoded as of now
            "user_ts": (new Date()).getTime(),
        })
        .then((response) => {
          setCurrentMessage("")
        })
        .catch((error) => {
          console.log(error);
        })
    };

    const receiveMessage = (message) => {
      console.log("RECEIVED", message)

      setMessages((prevMessages) => [...prevMessages, message]);
    };
    const onConnect = () => { console.log("CONNECTED TO SERVER ⚡️🔌")}

    return (
        // <div>
      <Hero
        channels={channels}
        currentMessage={currentMessage}
        setCurrentMessage={setCurrentMessage}
        setCurrentChannel={setCurrentChannel}
        sendMessage={sendMessage}
      />
    );
};

export default Message;