import { useclassNamete } from 'react'
import { BgSpots, MessageList, TabbedView } from './sundry'

export default function Hero({ channels, currentChannel, currentMessage, setCurrentMessage, sendMessage, setCurrentChannel }) {
  
  return (
    <div className="bg-white">
      <div className="relative isolate px-6 pt-14 lg:px-8">
        <BgSpots/>
        <div className="mx-auto max-w-2xl py-32 sm:py-32 lg:py-48">
          <div className="text-center">
            <h4 className="text-4xl font-bold tracking-tight text-gray-600 sm:text-5xl">
              Live Comments - Demo
            </h4>
            <input
                type="text"
                value={currentMessage}
                onChange={(e) => setCurrentMessage(e.target.value)}
            />
            <button onClick={sendMessage}>Send</button>
            <p className="mt-6 text-lg leading-8 text-gray-400">
              Select the channel to send message
            </p>
            <TabbedView channels={channels} currentChannel={currentChannel} setCurrentChannel={setCurrentChannel} />
          </div>
        </div>
      </div>
    </div>
  )
}
