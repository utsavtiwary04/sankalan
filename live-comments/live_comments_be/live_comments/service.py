from .tasks import save_comment
from .models import Channel, Comment
from .exceptions import EntityNotFound
from django_redis import get_redis_connection


def new_comment(data: dict):
	# import ipdb; ipdb.settrace()

	save_comment.delay(data)

	return data.values()

def past_comments(channel_id=None, count=10, start_ts=None, end_ts=None):

	channel = Channel.active_channel_by_id(channel_id)
	if not channel:
		raise EntityNotFound("channel", channel_id)

	return [c.to_json() for c in Comment.recent_comments(count=count, start_ts=start_ts, end_ts=start_ts, channel_id=channel_id)]


def get_user_comments(user_id, start_ts, end_ts):
	pass
