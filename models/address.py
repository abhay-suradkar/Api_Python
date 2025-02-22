from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database import Base  # Import Base only, no database imports

class Address(Base):
    __tablename__ = "address"

    address_id = Column(Integer, primary_key=True, autoincrement=False)  # ✅ Disable auto-increment
    state = Column(String(100), nullable=False)
    city = Column(String(100), nullable=False)
    area = Column(String(100), nullable=False)
    zip_code = Column(String(20), nullable=False)
    email = Column(String(100), ForeignKey("users.email", ondelete="CASCADE", onupdate="CASCADE"), nullable=False)
