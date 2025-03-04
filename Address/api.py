from fastapi import FastAPI, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from utils.database import SessionLocal, engine, get_db
from auth_utils import get_current_user_email
from Users.models import User
from Address.models import Address, Base
from Address.schemas import AddAddress, DeleteAddress
from Address.services import AddressService 
router = APIRouter()

class AddressAPI:
    @router.post("/addAddress")
    def add_address(address: AddAddress, db: Session = Depends(get_db), token: str = Depends(get_current_user_email)):        
        return AddressService.add_address(address, db)

    @router.get("/getaddress1")
    def get_address1(db : Session = Depends(get_db)):
        return AddressService.get_address1(db)


    @router.get("/getaddress")
    def get_address(email: str = None, db: Session = Depends(get_db)):
        return AddressService.get_address(email, db)

    @router.delete("/deleteaddress/{address_id}")
    def delete_address(address_id: str, db: Session = Depends(get_db)):
        return AddressService.delete_address(address_id, db)
