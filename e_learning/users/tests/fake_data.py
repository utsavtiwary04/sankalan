from users.models import User

fake_user_list = [
  {
    "name": "Rahul Patel",
    "phone": "9876543210",
    "email": "rahul.patel@example.com"
  },
  {
    "name": "Jennifer Smith",
    "phone": "1234567890",
    "email": "jennifer.smith@example.com"
  },
  {
    "name": "Amit Kumar",
    "phone": "9988776655",
    "email": "amit.kumar@example.com"
  },
  {
    "name": "Emily Johnson",
    "phone": "9876541230",
    "email": "emily.johnson@example.com"
  },
  {
    "name": "Samantha Williams",
    "phone": "7890123456",
    "email": "samantha.williams@example.com"
  },
  {
    "name": "Arun Sharma",
    "phone": "8765432109",
    "email": "arun.sharma@example.com"
  },
  {
    "name": "Olivia Davis",
    "phone": "2345678901",
    "email": "olivia.davis@example.com"
  },
  {
    "name": "Rajesh Gupta",
    "phone": "8765432101",
    "email": "rajesh.gupta@example.com"
  },
  {
    "name": "Daniel Brown",
    "phone": "3456789012",
    "email": "daniel.brown@example.com"
  },
  {
    "name": "Priya Patel",
    "phone": "9876543211",
    "email": "priya.patel@example.com"
  }
]

def create_dummy_users():
	for user_data in fake_user_list:
		new_user = User.objects.create(**user_data)
		new_user.save()

