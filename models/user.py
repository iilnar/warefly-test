from sqlalchemy import Column, Integer, String
from db import Base

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String(20), nullable=False)
    email = Column(String(20), nullable=False)
    password = Column(String(20), nullable=False)

    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.password = password
