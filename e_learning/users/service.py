from .models import User

def get_user(user_id: int):
	return User.objects.filter(id=user_id).filter(deleted_at=None).first()

def search_user(name: str):
	return User.objects.get(name__contains='name').all()
