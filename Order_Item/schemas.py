from pydantic import BaseModel, EmailStr, Field
from typing import List

class ProductItem(BaseModel):
    product_id: int
    product_name: str
    quantity: int
    price: float

class AddOrderItem(BaseModel):
    email: EmailStr
    products: List[ProductItem]

