import redis
import threading
import socketio

class DBListener(threading.Thread):
    def __init__(self, r, channels):
        threading.Thread.__init__(self)
        self.redis = r
        self.pubsub = self.redis.pubsub()
        self.pubsub.subscribe(channels)
    
    def work(self, item):
        ## Write to DB
        sio = socketio.Client()
        
        print(item['channel'], ":", item['data'])
    
    def run(self):
        for item in self.pubsub.listen():
            if item['data'] == "KILL": ## poison pill
                self.pubsub.unsubscribe()
                print(self, "unsubscribed and finished")
                break
            else:
                self.work(item)

if __name__ == "__main__":
    r = redis.Redis(host='localhost', port=6379, decode_responses=True)
    listener = DBListener(r, ['test'])
    listener.start()
