import { BgSpots, TabbedView } from './sundry'

export default function Hero({ channels, comments, currentMessage, setCurrentMessage, sendMessage, currentChannel, setCurrentChannel }) {
  
  return (
    <div className="bg-white">
      <div className="relative isolate px-6 pt-14 lg:px-8">
        <BgSpots/>
        <div className="mx-auto max-w-2xl py-8">
          <div className="text-center">
            <h4 className="text-4xl font-bold tracking-tight text-gray-600 sm:text-5xl">
              Live Comments - Demo
            </h4>
            <div className="my-12">
              <input
                className="border border-gray-400 rounded-sm"
                type="text"
                value={currentMessage}
                onChange={(e) => setCurrentMessage(e.target.value)}
              />
              <button
                type="button"
                className="text-white bg-gray-600 hover:bg-gray-600 font-small rounded-sm text-sm px-4 py-1 mx-2 my-4 dark:bg-gray-500"
                onClick={sendMessage}
              >
                Send ➢
              </button>
              <p className="mt-6 text-lg text-left leading-8 text-gray-400">
                Select a channel to comment
              </p>
              <TabbedView channels={channels} comments={comments} currentChannel={currentChannel} setCurrentChannel={setCurrentChannel} />
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}
