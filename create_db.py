from db import Base, engine, db_session
from models import User
from routes.auth import password_hash

if __name__ == '__main__':
    Base.metadata.create_all(engine)

    for i in range(10):
        email = 'mail_{}@mail.ru'.format(i)
        db_session.add(User('User_{}'.format(i), email, password_hash(email, 'pass')))
    db_session.commit()
