from sqlalchemy import Column, String, Float, ForeignKey, Integer, Computed, UUID
from utils.database import Base
from sqlalchemy.orm import relationship
from uuid import uuid4

class OrderItem(Base):
    __tablename__ = "order_items"

    order_item_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4, unique=True, nullable=False)
    product_name = Column(String, nullable=False)
    quantity = Column(Integer, nullable=False)
    price = Column(Float, nullable=False)
    product_id = Column(Integer, nullable=False)
    total_price = Column(Float, Computed("quantity * price", persisted=True), nullable=False)

    email = Column(String, ForeignKey("users.email"), nullable=False)

    user = relationship("User", back_populates="order_items")
