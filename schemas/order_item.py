from pydantic import BaseModel

class AddorderItem(BaseModel):
    order_item_id: int
    product_id: int
    product_name: str
    quantity: int
    price: int

    def total_price(self) -> int:
        return self.quantity * self.price

class DeleteorderItem(BaseModel):
    order_item_id: int
