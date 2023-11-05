'use client'
import { socket } from './client_socket';
import { get, post } from './api_requests';
import axios from 'axios';
import Hero from './hero';
import { useState, useEffect } from 'react';
import io from 'socket.io-client';

const BE_SERVER = "http://localhost:8000"
const URLS = {
  "activeChannels": `${BE_SERVER}/live-comments/channels/active`,
  "newComment":     `${BE_SERVER}/live-comments/comments/new`,
  "pastComments":   `${BE_SERVER}/live-comments/comments/past`
}
const LiveComments = () => {
  const [allChannels, setAllChannels]       = useState([])
  const [currentMessage, setCurrentMessage] = useState("")
  const [currentChannel, setChannel]        = useState(1)
  const [comments, setComments]             = useState({})

  useEffect(() => {
    const queryParams = {}
    const onError = r => {}
    const onSuccess = ({ data }) => { setAllChannels(data.data) }
    get(URLS.activeChannels, queryParams, onSuccess, onError)

    const _queryParams = { "channel_id": currentChannel, "count": 5 }
    const _onError = r => {}
    const _onSuccess = ({ data }) => { setComments({ ...comments, "channel_id": data.data  }) }
    get(URLS.pastComments, _queryParams, _onSuccess ,_onError)

    socket.connect()
    socket.on("connect", onConnect)
    socket.on('message', receiveMessage);
    return () => {
      socket.disconnect();
    };
  }, []);

  const setCurrentChannel = (channel_id) => {
    setChannel(channel_id)
    const _queryParams = { "channel_id": channel_id, "count": 5 }
    const _onError = r => {}
    const _onSuccess = ({ data }) => {
      console.log(data)
      setComments({ ...comments, "channel_id": data.data  })
    }
    get(URLS.pastComments, _queryParams, _onSuccess ,_onError)

  }

  const sendMessage = () => {
    const payload = {
        "channel_id" : currentChannel,
        "comment": currentMessage,
        "user_id": "1", //hardcoded
        "user_ts": (new Date()).getTime(),
    }
    const onError = () => {}
    const onSuccess = (response) => {
      setCurrentMessage("") 
    }
    post(URLS.newComment, payload, onSuccess, onError)
  };

  const receiveMessage = (message) => {
    const channel = message
    const channel_id = message.channel_id;

    setComments((prevComments) => {
      ...prevChannels,
      channel_id: message.messages
    });
  };
  const onConnect = () => { console.log("CONNECTED TO SERVER ⚡️🔌")}

  return (
    <Hero
      channels={allChannels}
      comments={comments}
      currentChannel={currentChannel}
      setCurrentChannel={setCurrentChannel}
      currentMessage={currentMessage}
      setCurrentMessage={setCurrentMessage}
      sendMessage={sendMessage}
    />
  );
};

export default LiveComments;
