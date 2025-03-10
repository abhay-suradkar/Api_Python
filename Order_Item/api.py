from sqlalchemy.orm import Session
from fastapi import FastAPI, Depends, APIRouter, HTTPException
from utils.database import get_db
from Order_Item.models import OrderItem
from Order_Item.services import OrderItemService
from Users.models import User
from Order_Item.schemas import AddOrderItem
from fastapi import APIRouter, Body

router = APIRouter()
  

class OrderItemAPI:

    @router.post("/add_order_item")
    def add_order_item(
    order_items: AddOrderItem = Body(...),  # ✅ Ensure FastAPI treats this as request body
    db: Session = Depends(get_db)):
        return OrderItemService.add_order_item(order_items, db)

    @router.get("/get_orderItem")
    def get_orderItem(db: Session = Depends(get_db)):
        return OrderItemService.get_orderItem(db)

    @router.get("/get_orderItem1")
    def get_orderItem1(email: str, db: Session = Depends(get_db)):
        return OrderItemService.get_orderItem1(email, db)