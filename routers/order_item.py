from fastapi import APIRouter, Depends, HTTPException, status 
from sqlalchemy.orm import Session
from utils.database import get_db
from models.order_item import OrderItem
from schemas.order_item import AddOrderItems
from Users.models import User
from collections import defaultdict


router = APIRouter()

def get_current_user_email(db: Session):
    """Fetches the logged-in user's email from the Users table."""
    user = db.query(User).first()  # Replace this with actual session-based user retrieval logic
    return user.email if user else None

@router.post("/add_order_items")
def add_order_items(
    order_items: AddOrderItems, 
    db: Session = Depends(get_db)
):
    """Add multiple order items for the logged-in user."""

    user_email = get_current_user_email(db)  
    if not user_email:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not logged in")

    if not order_items.items:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No items provided")

    order_item_id = order_items.items[0].order_item_id  # Take first item's order_item_id
    order_items_to_insert = []
    inserted_items = []

    for item in order_items.items:
        if item.order_item_id != order_item_id:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="All items must have the same order_item_id")
            
        order_item = OrderItem(
            email=user_email,
            order_item_id=order_item_id,
            product_id=item.product_id,
            product_name=item.product_name,
            quantity=item.quantity,
            price=item.price,
            total_price=item.price * item.quantity
        )

        order_items_to_insert.append(order_item)

        inserted_items.append({
            "product_id": item.product_id,
            "product_name": item.product_name,
            "price": item.price,
            "quantity": item.quantity,
            "total_price": order_item.total_price
        })

    db.add_all(order_items_to_insert)
    db.flush()  # Ensure objects are persisted before commit
    db.commit()

    return {
        "order_item_id": order_item_id,
        "items": inserted_items
    }

@router.get("/order-items", status_code=status.HTTP_200_OK)
def get_order_items(db: Session = Depends(get_db)):
    """Retrieve all order items from the database, grouped by order_item_id."""
    
    order_items = db.query(OrderItem).all()

    if not order_items:
        raise HTTPException(status_code=404, detail="No order items found.")

    # Group items by order_item_id
    grouped_orders = defaultdict(list)

    for item in order_items:
        grouped_orders[item.order_item_id].append({
            "product_id": item.product_id,
            "product_name": item.product_name,
            "quantity": item.quantity,
            "price": item.price,
            "total_price": item.total_price or (item.quantity * item.price),
        })

    return {
        "total_orders": len(grouped_orders),
        "orders": [
            {"order_item_id": order_id, "items": items}
            for order_id, items in grouped_orders.items()
        ]
    }

# # ✅ Delete Order Item by ID
# @router.delete("/order-items/{order_item_id}", status_code=status.HTTP_200_OK)
# def delete_order_item(order_item_id: int, db: Session = Depends(get_db)):
#     """Delete an order item by ID."""
    
#     existing_order_item = db.query(OrderItem).filter(OrderItem.order_item_id == order_item_id).first()

#     if not existing_order_item:
#         raise HTTPException(status_code=404, detail="Order item ID not found.")

#     try:
#         db.delete(existing_order_item)
#         db.commit()
#         return {"message": "Order item deleted successfully."}
#     except Exception as e:
#         db.rollback()
#         raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
