'use client'
import { socket } from './socket';
import { useState, useEffect } from 'react';
import io from 'socket.io-client';

const BE_SERVER = "http://localhost:3000"
const Message = () => {
    const [messages, setMessages] = useState(["-- start --"]);

    useEffect(() => {
      console.log(`URL trying to connect to : ${process.env.SOCKET_SERVER_URL}`)
      socket.connect()

      socket.on('message', receiveMessage);

      return () => {
        socket.disconnect();
      };
    }, []);

    const sendMessage = () => {
        axios.post(BE_SERVER, {
          // Add parameters here
        })
        .then((response) => {
          console.log(response.data);
        })
        .catch((error) => {
          console.log(error);
        })
    };

    const receiveMessage = (message) => {
      setMessages((prevMessages) => [...prevMessages, message]);
    };

    return (
        <div>
            <div>
                <u> HERE ARE THE MESSAGES👇🏻</u>
            </div>
            <br></br>
            {messages.map((message, index) => (
                <p key={index}>{message}</p>
            ))}

           {/* <input
                type="text"
                value={currentMessage}
                onChange={(e) => setCurrentMessage(e.target.value)}
            />
            <button onClick={sendMessage}>Send</button>*/}
        </div>
    );
};

export default Message;