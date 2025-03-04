from sqlalchemy import Column, Integer, String, Float, Computed, ForeignKey
from sqlalchemy.orm import relationship
from utils.database import Base

class OrderItem(Base):
    __tablename__ = "order_items"

    order_item_id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String(100), ForeignKey("users.email", ondelete="CASCADE", onupdate="CASCADE"), nullable=False)
    product_id = Column(Integer, nullable=False)  # ✅ No ForeignKey since it's just an identifier
    product_name = Column(String, nullable=False)
    quantity = Column(Integer, nullable=False)
    price = Column(Float, nullable=False)
    total_price = Column(Float, Computed("quantity * price", persisted=True), nullable=False)  # ✅ Correct Computed column

    user = relationship("User", back_populates="order_items")  # ✅ Remove extra indentation
