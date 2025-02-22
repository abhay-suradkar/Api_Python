from sqlalchemy import Column, String
from database import Base

class User(Base):
    __tablename__ = "users"

    email = Column(String(100), primary_key=True, unique=True, nullable=False)
    name = Column(String(100), nullable=False)
    mobile = Column(String(15), unique=True, nullable=False)
    password = Column(String, nullable=False)
