from fastapi import FastAPI, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from database import SessionLocal, engine
from models.user import  User
from models.address import Address, Base
from schemas.address import AddAddress, DeleteAddress

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/addAddress")
def add_address(address: AddAddress, db: Session = Depends(get_db)):
    user_exists = db.query(User).filter(User.email == address.email).first()
    if not user_exists:
        raise HTTPException(status_code=400, detail="User does not exist. Create a user first.")

    existing_address = db.query(Address).filter(Address.address_id == address.address_id).first()
    if existing_address:
        raise HTTPException(status_code=400, detail="Address already registered")

    new_address = Address(
        address_id=address.address_id,  # ✅ Explicitly set the address_id
        state=address.state,
        city=address.city,
        area=address.area,
        zip_code=address.zip_code,
        email=address.email,
    )

    db.add(new_address)
    db.commit()
    db.refresh(new_address)  

    return {"message": "Address registered successfully"}


@router.get("/getaddress")
def get_address(db: Session = Depends(get_db)):
    address = db.query(Address).all()
    address_data = [
        {
            "address_id": addr.address_id,
            "state": addr.state,
            "city": addr.city,
            "area": addr.area,
            "zip_code": addr.zip_code,
            "email": addr.email,
        } 
        for addr in address
    ]
    return {"total_address": len(address), "address": address_data}

@router.delete("/deleteaddress/{address_id}")
def delete_address(address_id: str, db: Session = Depends(get_db)):
    address = db.query(Address).filter(Address.address_id == address_id).first()
    if not address:
        raise HTTPException(status_code=404, detail="Address not found")
    db.delete(address)
    db.commit()
    return {"message": "Address Delete successfully"}
app = FastAPI()

app.include_router(router)
