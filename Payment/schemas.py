from pydantic import BaseModel, EmailStr

class PaymentRequest(BaseModel):
    amount: float
    buyer_name: str
    email: EmailStr
    phone: str