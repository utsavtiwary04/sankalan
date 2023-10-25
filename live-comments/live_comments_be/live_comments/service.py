from .models import User, Comment
from .tasks import test_task

def new_comment(data: dict):
	# test_task.delay()
	# user = User.active_user(data["user_id"])
	return data.values()



def get_channel_comments(channel, start_ts, end_ts):
	pass

def get_user_comments(user_id, start_ts, end_ts):
	pass