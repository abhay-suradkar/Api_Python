from fastapi import APIRouter
from .schemas import PaymentRequest
from .services import create_instamojo_payment

router = APIRouter(prefix="/payment", tags=["Payment"])

@router.post("/create-payment")
def create_payment(request: PaymentRequest):
    return create_instamojo_payment(request)
