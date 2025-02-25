from pydantic import BaseModel, field_validator
from typing import List

class AddOrderItem(BaseModel):  # ✅ Renamed to avoid duplication
    order_item_id: int
    product_id: int
    product_name: str
    quantity: int
    price: float  # ✅ Ensuring price is a float

    @field_validator("quantity")
    @classmethod
    def validate_quantity(cls, value):
        if value <= 0:
            raise ValueError("Quantity must be greater than zero.")
        return value

    @field_validator("price")
    @classmethod
    def validate_price(cls, value):
        if value < 0:
            raise ValueError("Price cannot be negative.")
        return value

    class Config:
        from_attributes = True  # ✅ Allows SQLAlchemy model conversion

class AddOrderItems(BaseModel):
    items: List[AddOrderItem]  # ✅ Corrected reference

class DeleteOrderItem(BaseModel):
    order_item_id: int
