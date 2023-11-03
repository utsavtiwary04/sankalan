import {Tabs, Tab, Card, CardBody, Chip} from "@nextui-org/react";

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

export function MessageList({ messages }) {
  return (
    <div>
      {
        messages.map((message, index) => (
          <div className="msg-bubble" key={index}>
            <div className="msg-info">
              <div className="msg-info-name">Sajad</div>
              <div className="msg-info-time">12:46</div>
            </div>

            <div className="msg-text">
              {message}
            </div>
          </div>
        ))
      }
    </div>
  );
};

export function TabbedView({ channels, currentChannel, setCurrentChannel }) {
  return (
    <div className="flex w-full flex-col">
      <Tabs 
        aria-label="Options" 
        color="primary" 
        variant="underlined"
        classNames={{
          tabList: "gap-6 w-full relative rounded-none p-0 border-b border-divider",
          cursor: "w-full bg-[#22d3ee]",
          tab: "max-w-fit px-0 h-12",
          tabContent: "group-data-[selected=true]:text-[rgb(255, 241, 207)]"
        }}
        onSelectionChange={setCurrentChannel}
      >
        {
          channels.map((channel, index) =>(
          <Tab
            key={`${channel.name}_${channel.id}`}
            title={
              <div className="flex items-center space-x-2">
                <span>{channel.name}</span>
                <Chip size="sm" variant="faded">9</Chip>
              </div>
            }
          >
            <Card>
                <CardBody>
                  <MessageList messages={channel.messages} />
                </CardBody>
            </Card>
          </Tab>))
      }
      </Tabs>
    </div>   
  );
}
