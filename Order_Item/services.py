from fastapi import APIRouter, Depends, HTTPException, Body
from sqlalchemy.orm import Session
import uuid
from Order_Item.models import OrderItem
from Order_Item.schemas import AddOrderItem
from Users.models import User
from utils.database import get_db
from fastapi import APIRouter, Body

router = APIRouter()

class OrderItemService:
    def add_order_item(
        order_items: AddOrderItem = Body(...),
        db: Session = Depends(get_db)):
            try:
                user = db.query(User).filter(User.email == order_items.email).first()
                if not user:
                    raise HTTPException(status_code=404, detail="User does not exist. Please create an account first.")

                if not order_items.products:
                    raise HTTPException(status_code=400, detail="No items provided")

                order_item_id = str(uuid.uuid4())
                order_items_to_insert = []
                total_price = 0

                for item in order_items.products:
                    items_total = item.price * item.quantity
                    total_price += items_total

                    new_order = OrderItem(
                        order_item_id=order_item_id,
                        product_id=item.product_id,
                        product_name=item.product_name,
                        quantity=item.quantity,
                        price=item.price,
                        email=user.email,
                        total_price=items_total
                    )

                    order_items_to_insert.append(new_order)

                db.add_all(order_items_to_insert)
                db.commit()

                return {
                    "order_item_id": order_item_id,
                    "email": user.email,
                    "products": [
                        {
                            "product_id": item.product_id,
                            "product_name": item.product_name,
                            "quantity": item.quantity,
                            "price": item.price,
                            "total_price": item.price * item.quantity
                        } for item in order_items.products
                    ],
                    "total_price": total_price
                }

            except Exception as e:
                db.rollback()
                raise HTTPException(status_code=500, detail=str(e))

    def get_orderItem(db: Session = Depends(get_db)):
        try:
            order_item = db.query(OrderItem).all()
            return order_item
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")

    
    def get_orderItem1(email: str, db: Session = Depends(get_db)):
        try:
            order_item_query = db.query(OrderItem)

            if email:  # Corrected spelling
                order_item_query = order_item_query.filter(OrderItem.email == email)

            order_items = order_item_query.all()  # Corrected variable name

            if not order_items:  # Fixed variable name
                raise HTTPException(status_code=404, detail="No order items found")

            order_item_data = [
                {
                    "order_item_id": str(ord_it.order_item_id),  
                    "product_name": ord_it.product_name,
                    "product_id": ord_it.product_id,
                    "quantity": ord_it.quantity,
                    "price": ord_it.price,
                    "total_price": ord_it.total_price,
                    "email": ord_it.email,
                }
                for ord_it in order_items  # Fixed variable name
            ]
            return {"total_order_item": len(order_items), "order_item": order_item_data}  # Fixed key name
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")
