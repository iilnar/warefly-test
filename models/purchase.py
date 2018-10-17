from sqlalchemy import Column, Integer, ForeignKey
from db import Base


class Purchase(Base):
    __tablename__ = 'purchases'

    id = Column(Integer, primary_key=True)
    price = Column(Integer, nullable=False) 
    product_id = Column(Integer, ForeignKey('products.id'))
    buyer_id = Column(Integer, ForeignKey('users.id'))
    store_id = Column(Integer, ForeignKey('stores.id'))

    def __init__(self, buyer_id: int, store_id: int, product_id: int, price: int):
        self.buyer_id = buyer_id
        self.store_id = store_id
        self.product_id = product_id
        self.price = price
