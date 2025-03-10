from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from utils.database import Base

class User(Base): 
    __tablename__ = "users"

    email = Column(String(100), primary_key=True)
    name = Column(String(100), nullable=False)
    mobile = Column(String(15), unique=True, nullable=False)
    password = Column(String, nullable=False)

    addresses = relationship("Address", back_populates="user")
    order_items = relationship("OrderItem", back_populates="user")
