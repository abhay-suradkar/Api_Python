from fastapi import FastAPI, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from database import SessionLocal  
from models.orders import Orders
from models.user import User
from models.address import Address
from schemas.orders import CreateOrders, UpdateOrders,DeleteOrders # ✅ Schema for validation

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/createOrders")
def create_order(orders: CreateOrders, db: Session = Depends(get_db)):
    user_exist = db.query(User).filter(User.email == orders.email).first()
    if not user_exist:
        raise HTTPException(status_code=400, detail="User does not exist. Create a user first.")

    address_exist = db.query(Address).filter(Address.address_id == orders.address_id).first()
    if not address_exist:
        raise HTTPException(status_code=400, detail="Address does not exist. Create an address first.")

    existing_order = db.query(Orders).filter(Orders.order_id == orders.order_id).first()
    if existing_order:
        raise HTTPException(status_code=400, detail="Order ID already exists. Choose a unique order_id.")

    new_order = Orders(**orders.dict())

    db.add(new_order)
    db.commit()
    db.refresh(new_order)

    return {"message": "Order registered successfully", "order_id": new_order.order_id}

@router.get("/getOrders")
def get_orders(db:Session = Depends(get_db)):
    orders = db.query(Orders).all()
    orders_data = [
        {
            "order_id": ord.order_id,
            "total_amount":ord.total_amount,
            "order_status":ord.order_status,
            "address_id": ord.address_id,
            "email": ord.email,
        }
        for ord in orders
    ]
    return {"total_address": len(orders), "address": orders_data}

@router.put("/putOrders")
def put_Orders(data : UpdateOrders, db:Session= Depends(get_db)):

    orders = db.query(Orders).filter(Orders.order_id == data.order_id).first()

    if not orders:
        raise HTTPException(status_code= 404, detail="Orders is not found")

    if orders:
        orders.order_status = data.order_status

    db.commit()
    db.refresh(orders)

    return {"message": "Order updated successfully", "updated_order": orders}


@router.delete("/deleteOrder/{order_id}")
def delete_order(order_id: int, db: Session = Depends(get_db)):
    order = db.query(Orders).filter(Orders.order_id == order_id).first()

    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    db.delete(order)
    db.commit()

    return {"message": "Order deleted successfully"}
