from sqlalchemy import Column, Integer, String
from db import Base

class Product(Base):
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True)
    name = Column(String(20), nullable=False)
    vendor = Column(String(20), nullable=False)

    def __init__(self, name, vendor):
        self.name = name
        self.vendor = vendor
