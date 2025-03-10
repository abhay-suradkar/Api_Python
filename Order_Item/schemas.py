from pydantic import BaseModel
from typing import List

class ProductItem(BaseModel):
    product_id: int
    product_name: str
    quantity: int
    price: float

class AddOrderItem(BaseModel):
    email: str
    products: List[ProductItem]
