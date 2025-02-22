from pydantic import BaseModel, EmailStr

class AddAddress(BaseModel):
    address_id: int  # ✅ Change from string to integer
    state: str  
    city: str   
    area: str   
    zip_code: str  # ✅ Keep as string since ZIP codes may start with 0
    email: EmailStr    

class DeleteAddress(BaseModel):
    address_id: int  # ✅ Change from string to integer
