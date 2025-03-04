from sqlalchemy import Column, Integer, String, ForeignKey, UUID
from sqlalchemy.orm import relationship
from utils.database import Base  # Import Base only, no database imports
from uuid import uuid4

class Address(Base):
    __tablename__ = "address"

    address_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4, unique=True, nullable = False)
    state = Column(String(100), nullable=False)
    city = Column(String(100), nullable=False)
    area = Column(String(100), nullable=False)
    zip_code = Column(String(20), nullable=False)
    email = Column(String(100), ForeignKey("users.email", ondelete="CASCADE", onupdate="CASCADE"), nullable=False)
