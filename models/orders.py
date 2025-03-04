from sqlalchemy import Column, Integer, String, ForeignKey, Float
from utils.database import Base  # ✅ Ensure 'Base' is correctly imported

class Orders(Base):
    __tablename__ = "orders"

    order_id = Column(Integer, primary_key=True, autoincrement=False)  # ✅ Make sure this matches your database schema
    email = Column(String, ForeignKey("users.email"), nullable=False)
    total_amount = Column(Float, nullable=False)
    order_status = Column(String, default="Pending")
    address_id = Column(Integer, ForeignKey("address.address_id"), nullable=False)
