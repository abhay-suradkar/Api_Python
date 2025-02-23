from sqlalchemy import Column, Integer, ForeignKey, Computed, String, Float
from sqlalchemy.orm import relationship
from database import Base

class OrderItem(Base):
    __tablename__ = "order_items"

    order_item_id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, nullable=False)  
    product_name = Column(String, nullable=False)
    quantity = Column(Integer, nullable=False)
    price = Column(Integer, nullable=False)
    total_price = Column(Float, Computed("quantity * price"))
   