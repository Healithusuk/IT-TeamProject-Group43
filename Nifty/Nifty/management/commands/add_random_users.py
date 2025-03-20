from faker import Faker
import random
from allModels.models import Accounts

fake = Faker()

num_users = 100  

for _ in range(num_users):
    username = fake.user_name()
    email = fake.email()
    first_name = fake.first_name()
    last_name = fake.last_name()
    user = Accounts.objects.create_user(
        username=username,
        email=email,
        password='nifty',
        first_name=first_name,
        last_name=last_name,
    )
    print(f"Created user: {username}")
