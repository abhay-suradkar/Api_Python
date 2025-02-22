from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal, get_db
from models.order_item import OrderItem
from models.orders import Orders
from schemas.order_item import AddorderItem, DeleteorderItem # ✅ Correct import

router = APIRouter()

@router.post("/Addorder_item")
def add_order_item(order_item: AddorderItem, db: Session = Depends(get_db)):
    # Check if the order exists
    order_exists = db.query(Orders).filter(Orders.order_id == order_item.order_id).first()
    if not order_exists:
        raise HTTPException(status_code=400, detail="Order does not exist. Create an order first.")

    # Check if the order item already exists
    existing_order_item = db.query(OrderItem).filter(OrderItem.order_item_id == order_item.order_item_id).first()
    if existing_order_item:
        raise HTTPException(status_code=400, detail="Order item already exists.")

    # ✅ Calculate total_price dynamically
    total_price = order_item.quantity * order_item.price

    # Create new order item
    new_order_item = OrderItem(
        order_item_id=order_item.order_item_id,
        order_id=order_item.order_id,
        product_id= order_item.order_id,
        product_name=order_item.product_name,
        quantity=order_item.quantity,
        price=order_item.price,
        total_price=total_price,  # ✅ Assign calculated total price
    )

    db.add(new_order_item)
    db.commit()
    db.refresh(new_order_item)

    return {"message": "Order item registered successfully.", "total_price": total_price}


@router.get("/get")
def get_order_item(db: Session = Depends(get_db)):
    order_items = db.query(OrderItem).all()
    
    order_item_data = [
        {
            "order_item_id": ord.order_item_id,
            "order_id": ord.order_id,
            "product_id": ord.product_id,
            "product_name": ord.product_name,
            "quantity": ord.quantity,
            "price": ord.price,
            "total_price": ord.total_price if hasattr(ord, "total_price") else ord.quantity * ord.price,
        }
        for ord in order_items
    ]
    
    return {"total_order_items": len(order_items), "order_items": order_item_data}

@router.delete("/deleteorderitem/{order_item_id}")
def delete_order_item(order_item_id: int, db: Session = Depends(get_db)):
    existing_order_item = db.query(OrderItem).filter(OrderItem.order_item_id == order_item_id).first()

    if not existing_order_item:
        raise HTTPException(status_code=400, detail="Order Item ID not found. Create an order item first.")

    db.delete(existing_order_item)  # Pass the object, not the ID
    db.commit()  # Commit the transaction

    return {"message": "Order Item deleted successfully"}
