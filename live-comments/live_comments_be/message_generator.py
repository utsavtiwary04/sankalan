import uuid
import random

def generate_message(word_length=4)
	return " ".join([str(uuid.uuid4().hex[0:word_length]) for i in range(0,random.randint(1,7))])

def send_messages(url, rate=100):
	messages = [generate_message() for i in range(rate)]
	map(messages, lambda x: requests.post(url, data=x))
