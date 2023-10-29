from .tasks import save_comment
from django_redis import get_redis_connection


def new_comment(data: dict):


	# import ipdb; ipdb.settrace()

	save_comment.delay(data)

	return data.values()


def get_channel_comments(channel, start_ts, end_ts):
	pass


def get_user_comments(user_id, start_ts, end_ts):
	pass