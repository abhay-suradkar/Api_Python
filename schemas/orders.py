from pydantic import BaseModel, EmailStr
from typing import Optional

class CreateOrders(BaseModel):
    order_id: int
    email: EmailStr
    total_amount: float
    order_status: Optional[str] = "Pending"  # ✅ Default value
    address_id: int

class UpdateOrders(BaseModel):
    order_id: int
    order_status: str

class DeleteOrders(BaseModel):
    order_id: int
