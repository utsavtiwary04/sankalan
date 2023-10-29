import redis
import threading

class Listener(threading.Thread):
    def __init__(self, r, channels):
        threading.Thread.__init__(self)
        self.redis = r
        self.pubsub = self.redis.pubsub()
        self.pubsub.subscribe(channels)
    
    def work(self, item):
        ## listen to DB changes and push to socket
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
    client = Listener(r, ['test'])
    client.start()
