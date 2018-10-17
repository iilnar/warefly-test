import sqlite3

from db import Base, engine, Session
from models import User


if __name__ == '__main__':
    Base.metadata.create_all(engine)

    session = Session()
    for i in range(10):
        session.add(User('User_{}'.format(i), 'mail_{}@mail.ru'.format(i), 'pass'))
    session.commit()
