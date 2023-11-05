import {Tabs, Tab, Card, CardBody, Chip} from "@nextui-org/react";

function Loading({ alert }){
  return (
    <div className="container mx-auto py-12">{alert}</div>
  );
}

function formatDateTime(ts) {
  const date = new Date(ts);
  let h = date.getHours();
  let m = date.getMinutes();
  var meridian = h >= 12 ? "PM" : "AM";
  h = h % 12;
  h = h ? h : 12;
  m = m < 10 ? "0" + m : m;
  var strTime = h + ":" + m + ":" + meridian;
  return `${date.toDateString()} ${strTime}`
}

export function BgSpots(){
  return(
    <div
      className="absolute inset-x-0 -top-40 -z-10 transform-gpu overflow-hidden blur-3xl sm:-top-80"
      aria-hidden="true"
    >
      <div
          className="relative left-[calc(50%-11rem)] aspect-[1155/678] w-[36.125rem] -translate-x-1/2 rotate-[30deg] bg-gradient-to-tr from-[#ff80b5] to-[#9089fc] opacity-30 sm:left-[calc(50%-30rem)] sm:w-[72.1875rem]"
          style={{
            clipPath:
              'polygon(74.1% 44.1%, 100% 61.6%, 97.5% 26.9%, 85.5% 0.1%, 80.7% 2%, 72.5% 32.5%, 60.2% 62.4%, 52.4% 68.1%, 47.5% 58.3%, 45.2% 34.5%, 27.5% 76.7%, 0.1% 64.9%, 17.9% 100%, 27.6% 76.8%, 76.1% 97.7%, 74.1% 44.1%)',
          }}
      />
    </div>
  );
};

export function TabbedView({ channels, comments, currentChannel, setCurrentChannel }) {
  return (
    <div className="flex w-full flex-col">
      <div  className="flex items-center space-x-2">
        {
          !isEmpty(channels)? (channels.map((channel, index) => (
          <div
            key={`${channel.name}_${index}`}
          >
            <Card>
              <button
                className={`bg-blue-500 text-white font-bold py-2 px-4 border-b-4 rounded ${currentChannel == channel.id ? 'bg-red-500 border-red-700 ': 'border-blue-700'}`} 
                title={channel.id}
                key={channel.name}
                onClick={e => setCurrentChannel(e.currentTarget.title)}
              >
                <span>{channel.name}</span>
              </button>
            </Card>
          </div>))) : (<Loading alert="Loading Channels ..." />)
        }
      </div>
      <div className="focus:border-gray-300">
        <Card>
          <CommentsList comments={comments.channel_id} channel={currentChannel} />
        </Card>
      </div>
    </div>   
  );
}

function CommentsList({ comments, channel }) {
  return (
    <div>
      {
        !isEmpty(comments) ? (
          comments.map((comment, index) => (
            <div className="msg-bubble" key={`${channel.id}_msg_${index}`}>
              <div className="msg-info">
                <div className="msg-info-name">{comment.username}</div>
                <div className="msg-info-time">{formatDateTime(comment.time)}</div>
              </div>
              <div className="msg-text">
                {comment.comment}
              </div>
            </div>)
          )
        ) : (<Loading alert="No comments found 🫙"/>)
      }
    </div>
  );
};

const isEmpty = val => (val == null || val.length == 0)

