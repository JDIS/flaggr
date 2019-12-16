"""Users seeding data"""
from JDISCTF.models import Event, User


def get_records(events: [Event]):
    """Get the records to add to the database"""
    users = []
    for _ in events:
        user1 = User(email='test@test.com', username='test')
        user1.set_password('test')
        users.append(user1)
        user2 = User(email='test2@test.com', username='test2')
        user2.set_password('test')
        users.append(user2)
        user3 = User(email='test3@test.com', username='test3')
        user3.set_password('test')
        users.append(user3)
        user4 = User(email='test4@test.com', username='test4')
        user4.set_password('test')
        users.append(user4)

    user = User(email='admin@admin.com', username='admin')
    user.set_password('admin')
    users.append(user)
    user = User(email='admin2@admin.com', username='admin2')
    user.set_password('admin2')
    users.append(user)
    user = User(email='admin3@admin.com', username='admin3')
    user.set_password('admin3')
    users.append(user)
    user = User(email='admin4@admin.com', username='admin4')
    user.set_password('admin4')
    users.append(user)

    return users


FILTER_ARGS = {'username', 'email'}
