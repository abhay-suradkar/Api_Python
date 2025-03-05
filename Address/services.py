from fastapi import FastAPI, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from utils.database import SessionLocal, engine, get_db
from auth_utils import get_current_user_email
from Users.models import User
from Address.models import Address, Base
from Address.schemas import AddAddress, DeleteAddress
import uuid

class AddressService:

    def add_address(address: AddAddress, db: Session = Depends(get_db), email: str = Depends(get_current_user_email)):
        try:
            if not email:  # ✅ If token is None, user is not logged in
                raise HTTPException(status_code=401, detail="User not authenticated")

            new_address = Address(
                state=address.state,
                city=address.city,
                area=address.area,
                zip_code=address.zip_code,
                email=email,  # ✅ Email from token
            )

            db.add(new_address)
            db.commit()
            db.refresh(new_address)  
            return {"id": str(new_address.address_id), "message": "Address registered successfully"}

        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")

    def get_address1(db : Session = Depends(get_db)):
        try:
            address = db.query(Address).all()
            return address
        except Exception as e:
            print(e)

    def get_address(email: str, db: Session = Depends(get_db)):
        try:
            address_query = db.query(Address)

            if email:
                address_query = address_query.filter(Address.email == email)
        
            addresses = address_query.all()
            if not addresses:
                raise HTTPException(status_code=404, detail="No Addresses found")

            address_data = [
                {
                    "address_id": str(addr.address_id),
                    "state": addr.state,
                    "city": addr.city,
                    "area": addr.area,
                    "zip_code": addr.zip_code,
                    "email": addr.email,
                } 
                for addr in addresses  # Loop through fetched data, not query object
            ]
            return {"total_address": len(addresses), "address": address_data}
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

    def delete_address(address_id: str, db: Session = Depends(get_db)):
        try:
            address = db.query(Address).filter(Address.address_id == address_id).first()
            if not address:
                raise HTTPException(status_code=404, detail="Address not found")
            db.delete(address)
            db.commit()
            return {"message": "Address Delete successfully"}
        except Exception as e:
            print(e)

